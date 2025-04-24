"""
Collecteur d'avis critiques automobiles avec protection anti-piratage
"""

import re
import json
import hashlib
import logging
import sqlite3
import requests
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from ratelimit import limits, sleep_and_retry
from requests.exceptions import RequestException, Timeout, TooManyRedirects
from ..license_manager import LicenseManager, check_security

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reviews_collector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecurityConfig:
    """Configuration de sécurité pour le collecteur."""
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 10
    RATE_LIMIT_CALLS = 30
    RATE_LIMIT_PERIOD = 60
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    ALLOWED_SCHEMES = {'http', 'https'}
    ALLOWED_CONTENT_TYPES = {
        'text/html',
        'application/xhtml+xml',
        'application/xml'
    }

class ReviewsCollector:
    def __init__(self, db_path: str, license_key: str):
        """
        Initialise le collecteur avec protection anti-piratage.
        
        Args:
            db_path: Chemin vers la base de données SQLite
            license_key: Clé de licence valide
        """
        # Vérifier la sécurité
        security_ok, security_msg = check_security()
        if not security_ok:
            raise RuntimeError(f"Violation de sécurité: {security_msg}")
            
        # Vérifier la licence
        self.license_manager = LicenseManager(license_key)
        license_valid, license_msg = self.license_manager.verify_license()
        if not license_valid:
            raise RuntimeError(f"Licence invalide: {license_msg}")
            
        # Activer la protection du code
        self.license_manager.protect_code()
        
        self._validate_db_path(db_path)
        self.db_path = db_path
        
        # Chiffrer les données sensibles
        self.sources = self._encrypt_sources({
            'caradisiac': {
                'base_url': 'https://www.caradisiac.com/essai-auto/',
                'review_pattern': r'/essai-auto/',
                'search_pattern': lambda brand, model: f"{brand}-{model}".lower().replace(' ', '-')
            },
            'largus': {
                'base_url': 'https://www.largus.fr/essai/',
                'review_pattern': r'/essai-',
                'search_pattern': lambda brand, model: f"{brand}-{model}".lower().replace(' ', '-')
            },
            'autoplus': {
                'base_url': 'https://www.autoplus.fr/essai/',
                'review_pattern': r'/essai/',
                'search_pattern': lambda brand, model: f"{brand}/{model}".lower().replace(' ', '-')
            },
            'turbo': {
                'base_url': 'https://www.turbo.fr/essais-auto/',
                'review_pattern': r'/essai-',
                'search_pattern': lambda brand, model: f"{brand}-{model}".lower().replace(' ', '-')
            },
            'automobile-magazine': {
                'base_url': 'https://www.automobile-magazine.fr/essais/',
                'review_pattern': r'/essai/',
                'search_pattern': lambda brand, model: f"{brand}-{model}".lower().replace(' ', '-')
            }
        })
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'DNT': '1',
            'Sec-Fetch-Mode': 'navigate'
        }
        
        self._init_database()
        
        # Vérifier l'intégrité des données collectées
        self._verify_data_integrity()

    def _encrypt_sources(self, sources: Dict) -> bytes:
        """Chiffre les sources de données."""
        return self.license_manager._encrypt_data(sources)

    def _decrypt_sources(self) -> Dict:
        """Déchiffre les sources de données."""
        return self.license_manager._decrypt_data(self.sources)

    def _validate_db_path(self, db_path: str) -> None:
        """Valide le chemin de la base de données."""
        if not isinstance(db_path, str):
            raise ValueError("Le chemin de la base de données doit être une chaîne de caractères")
        
        db_dir = Path(db_path).parent
        if not db_dir.exists():
            raise ValueError(f"Le répertoire {db_dir} n'existe pas")
        
        if not db_dir.is_dir():
            raise ValueError(f"{db_dir} n'est pas un répertoire")

    def _init_database(self) -> None:
        """Initialise la base de données avec des contraintes de sécurité."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('PRAGMA foreign_keys = ON')
                conn.execute('PRAGMA journal_mode = WAL')
                conn.execute('PRAGMA synchronous = NORMAL')
                
                # Table pour stocker l'historique des requêtes
                conn.execute('''
                CREATE TABLE IF NOT EXISTS request_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    error_message TEXT,
                    UNIQUE(url, timestamp)
                )
                ''')
                
                # Table pour les avis avec validation des données
                conn.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_id INTEGER NOT NULL,
                    source TEXT NOT NULL CHECK(length(source) <= 50),
                    url TEXT NOT NULL CHECK(length(url) <= 500),
                    year INTEGER CHECK(year BETWEEN 2000 AND 2100),
                    positive_point TEXT CHECK(length(positive_point) <= 1000),
                    negative_point TEXT CHECK(length(negative_point) <= 1000),
                    date_collected TEXT NOT NULL,
                    hash TEXT UNIQUE NOT NULL,
                    FOREIGN KEY (model_id) REFERENCES models (id) ON DELETE CASCADE,
                    UNIQUE(model_id, source, positive_point, negative_point)
                )
                ''')
                
                # Index pour optimiser les requêtes
                conn.execute('CREATE INDEX IF NOT EXISTS idx_reviews_model ON reviews(model_id)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_reviews_source ON reviews(source)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_reviews_year ON reviews(year)')
                
        except sqlite3.Error as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
            raise

    @sleep_and_retry
    @limits(calls=SecurityConfig.RATE_LIMIT_CALLS, period=SecurityConfig.RATE_LIMIT_PERIOD)
    def _make_request(self, url: str, retry_count: int = 0) -> Optional[requests.Response]:
        """
        Effectue une requête HTTP sécurisée avec limitation de débit.
        
        Args:
            url: URL à requêter
            retry_count: Nombre de tentatives effectuées
            
        Returns:
            Response object ou None en cas d'échec
        """
        try:
            # Valider l'URL
            parsed_url = urlparse(url)
            if parsed_url.scheme not in SecurityConfig.ALLOWED_SCHEMES:
                logger.warning(f"Schéma d'URL non autorisé: {url}")
                return None
            
            response = requests.get(
                url,
                headers=self.headers,
                timeout=SecurityConfig.REQUEST_TIMEOUT,
                verify=True,  # Vérifie le certificat SSL
                allow_redirects=True,
                stream=True  # Pour vérifier la taille avant de télécharger
            )
            
            # Vérifier la taille du contenu
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > SecurityConfig.MAX_CONTENT_LENGTH:
                logger.warning(f"Contenu trop volumineux: {url}")
                return None
            
            # Vérifier le type de contenu
            content_type = response.headers.get('content-type', '').lower()
            if not any(allowed_type in content_type for allowed_type in SecurityConfig.ALLOWED_CONTENT_TYPES):
                logger.warning(f"Type de contenu non autorisé: {content_type}")
                return None
            
            response.raise_for_status()
            return response
            
        except (RequestException, Timeout, TooManyRedirects) as e:
            logger.error(f"Erreur lors de la requête {url}: {str(e)}")
            if retry_count < SecurityConfig.MAX_RETRIES:
                time.sleep(2 ** retry_count)  # Backoff exponentiel
                return self._make_request(url, retry_count + 1)
            return None

    def _clean_text(self, text: str) -> str:
        """Nettoie et sanitize le texte."""
        if not isinstance(text, str):
            return ""
        
        # Supprimer les caractères non imprimables
        text = ''.join(char for char in text if char.isprintable())
        
        # Nettoyer les espaces
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Limiter la longueur
        return text[:1000]

    def _extract_sentiment(self, text: str) -> Dict[str, List[str]]:
        """Extrait les sentiments de manière sécurisée."""
        if not text or not isinstance(text, str):
            return {'positives': [], 'negatives': []}
        
        positives = []
        negatives = []
        
        # Patterns sécurisés avec limite de longueur
        pos_patterns = [
            r'(?:avantages?|points? fort|qualités?|points? positifs?).*?[:]\s*(.*?)(?=\.|$)',
            r'(?:nous (?:avons )?aimé|on aime|j\'aime).*?[:]\s*(.*?)(?=\.|$)',
            r'(?:excellent|remarquable|parfait).*?[:]\s*(.*?)(?=\.|$)',
            r'(?:points? fort|forces?).*?[:]\s*(.*?)(?=\.|$)',
            r'(?:atouts?|succès).*?[:]\s*(.*?)(?=\.|$)'
        ]
        
        neg_patterns = [
            r'(?:inconvénients?|points? faible|défauts?|points? négatifs?).*?[:]\s*(.*?)(?=\.|$)',
            r'(?:nous (?:n\'avons )?pas aimé|on (?:n\')?aime pas|je (?:n\')?aime pas).*?[:]\s*(.*?)(?=\.|$)',
            r'(?:décevant|regrettable|dommage).*?[:]\s*(.*?)(?=\.|$)',
            r'(?:points? faible|faiblesses?).*?[:]\s*(.*?)(?=\.|$)',
            r'(?:limites?|problèmes?).*?[:]\s*(.*?)(?=\.|$)'
        ]
        
        try:
            # Extraction sécurisée des points positifs
            for pattern in pos_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    point = self._clean_text(match.group(1))
                    if point and len(point) > 10:
                        positives.append(point)
            
            # Extraction sécurisée des points négatifs
            for pattern in neg_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    point = self._clean_text(match.group(1))
                    if point and len(point) > 10:
                        negatives.append(point)
            
            # Analyse de secours si aucun point trouvé
            if not positives and not negatives:
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    sentence = self._clean_text(sentence)
                    if len(sentence) > 20:
                        if any(word in sentence.lower() for word in [
                            'excellent', 'remarquable', 'confortable',
                            'agréable', 'qualité', 'réussi'
                        ]):
                            positives.append(sentence)
                        elif any(word in sentence.lower() for word in [
                            'décevant', 'problème', 'défaut',
                            'manque', 'regrettable'
                        ]):
                            negatives.append(sentence)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des sentiments: {e}")
            return {'positives': [], 'negatives': []}
        
        return {
            'positives': list(set(positives))[:5],  # Limiter à 5 points
            'negatives': list(set(negatives))[:5]   # Limiter à 5 points
        }

    def _generate_review_hash(self, review: Dict[str, Any]) -> str:
        """Génère un hash unique pour un avis."""
        content = f"{review['source']}{review['url']}{review['year']}"
        content += ''.join(review['positives'])
        content += ''.join(review['negatives'])
        return hashlib.sha256(content.encode()).hexdigest()

    def _verify_data_integrity(self) -> None:
        """Vérifie l'intégrité des données collectées."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Vérifier les hashes des avis
                cursor.execute('SELECT id, source, url, year, positive_point, negative_point, hash FROM reviews')
                for row in cursor.fetchall():
                    review_id, source, url, year, pos, neg, stored_hash = row
                    
                    # Recalculer le hash
                    content = f"{source}{url}{year}"
                    if pos: content += pos
                    if neg: content += neg
                    calculated_hash = hashlib.sha256(content.encode()).hexdigest()
                    
                    # Vérifier la correspondance
                    if calculated_hash != stored_hash:
                        logger.error(f"Intégrité compromise pour l'avis {review_id}")
                        cursor.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
                
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Erreur lors de la vérification de l'intégrité: {e}")
            raise

    def collect_reviews(self, brand: str, model: str, year: int) -> List[Dict[str, Any]]:
        """
        Collecte les avis de manière sécurisée.
        
        Args:
            brand: Marque du véhicule
            model: Modèle du véhicule
            year: Année du modèle
            
        Returns:
            Liste des avis collectés
        """
        # Vérifier la licence à chaque collecte
        license_valid, _ = self.license_manager.verify_license()
        if not license_valid:
            raise RuntimeError("Licence invalide")
            
        # Vérifier la sécurité
        security_ok, security_msg = check_security()
        if not security_ok:
            raise RuntimeError(f"Violation de sécurité: {security_msg}")
        
        if not all(isinstance(x, str) for x in [brand, model]):
            raise ValueError("La marque et le modèle doivent être des chaînes de caractères")
        
        if not isinstance(year, int) or not (2000 <= year <= 2100):
            raise ValueError("L'année doit être un entier entre 2000 et 2100")
        
        reviews = []
        sources = self._decrypt_sources()
        
        for source_name, source_data in sources.items():
            try:
                search_term = source_data['search_pattern'](brand, model)
                search_url = urljoin(source_data['base_url'], search_term)
                
                response = self._make_request(search_url)
                if not response:
                    continue
                
                soup = BeautifulSoup(response.text, 'lxml')
                review_links = soup.find_all('a', href=re.compile(source_data['review_pattern']))
                
                for link in review_links[:3]:
                    try:
                        review_url = link.get('href')
                        if not review_url:
                            continue
                            
                        review_url = urljoin(source_data['base_url'], review_url)
                        review_response = self._make_request(review_url)
                        
                        if review_response:
                            review_soup = BeautifulSoup(review_response.text, 'lxml')
                            
                            content = None
                            for selector in ['article', '.content', '.article-content', '.post-content']:
                                content = review_soup.find(class_=selector)
                                if content:
                                    break
                            
                            if not content:
                                content = review_soup.find('article') or review_soup.find('div', class_='content')
                            
                            if content:
                                text = content.get_text()
                                sentiment = self._extract_sentiment(text)
                                
                                if sentiment['positives'] or sentiment['negatives']:
                                    review = {
                                        'source': source_name,
                                        'url': review_url,
                                        'year': year,
                                        'positives': sentiment['positives'],
                                        'negatives': sentiment['negatives'],
                                        'date_collected': datetime.now().isoformat()
                                    }
                                    review['hash'] = self._generate_review_hash(review)
                                    reviews.append(review)
                    
                    except Exception as e:
                        logger.error(f"Erreur lors de la collecte de l'avis {review_url}: {str(e)}")
                        continue
                
            except Exception as e:
                logger.error(f"Erreur lors de la collecte depuis {source_name}: {str(e)}")
                continue
            
            time.sleep(2)
        
        return reviews

    def save_reviews_to_db(self, reviews: List[Dict[str, Any]], model_id: int) -> None:
        """
        Sauvegarde les avis dans la base de données de manière sécurisée.
        
        Args:
            reviews: Liste des avis à sauvegarder
            model_id: ID du modèle dans la base de données
        """
        # Vérifier la licence avant la sauvegarde
        license_valid, _ = self.license_manager.verify_license()
        if not license_valid:
            raise RuntimeError("Licence invalide")
        
        if not isinstance(model_id, int) or model_id <= 0:
            raise ValueError("L'ID du modèle doit être un entier positif")
        
        if not isinstance(reviews, list):
            raise ValueError("Les avis doivent être fournis sous forme de liste")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('PRAGMA foreign_keys = ON')
                cursor = conn.cursor()
                
                # Vérifier que le modèle existe
                cursor.execute('SELECT 1 FROM models WHERE id = ?', (model_id,))
                if not cursor.fetchone():
                    raise ValueError(f"Le modèle avec l'ID {model_id} n'existe pas")
                
                for review in reviews:
                    try:
                        # Insérer les points positifs
                        for positive in review['positives']:
                            cursor.execute('''
                            INSERT OR IGNORE INTO reviews 
                            (model_id, source, url, year, positive_point, date_collected, hash)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                model_id,
                                review['source'][:50],
                                review['url'][:500],
                                review['year'],
                                positive[:1000],
                                review['date_collected'],
                                review['hash']
                            ))
                        
                        # Insérer les points négatifs
                        for negative in review['negatives']:
                            cursor.execute('''
                            INSERT OR IGNORE INTO reviews 
                            (model_id, source, url, year, negative_point, date_collected, hash)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                model_id,
                                review['source'][:50],
                                review['url'][:500],
                                review['year'],
                                negative[:1000],
                                review['date_collected'],
                                review['hash']
                            ))
                            
                    except sqlite3.Error as e:
                        logger.error(f"Erreur lors de l'insertion de l'avis: {str(e)}")
                        continue
                
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Erreur lors de la sauvegarde des avis: {str(e)}")
            raise
