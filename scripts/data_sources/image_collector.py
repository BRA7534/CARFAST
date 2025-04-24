import requests
import os
import time
from typing import Optional, List, Dict
from PIL import Image
import io
from .config import IMAGE_SOURCES
import hashlib

class ImageCollector:
    def __init__(self, save_dir: str):
        self.save_dir = save_dir
        self.session = requests.Session()
        self.rate_limit_delay = 1
        
        # Créer les sous-dossiers nécessaires
        for subdir in ['brands', 'vehicles', 'colors']:
            os.makedirs(os.path.join(save_dir, subdir), exist_ok=True)

    def download_brand_logo(self, brand: str) -> Optional[str]:
        """Télécharge le logo d'une marque."""
        save_path = os.path.join(self.save_dir, 'brands', f"{brand.lower()}.png")
        
        # Essayer d'abord carlogos.org
        logo_url = IMAGE_SOURCES['BRANDS']['base_url'] + IMAGE_SOURCES['BRANDS']['format'].format(brand=brand.lower())
        if self._download_and_save_image(logo_url, save_path):
            return save_path
            
        # Si échec, essayer Wikimedia
        wiki_url = f"{IMAGE_SOURCES['WIKIMEDIA']['base_url']}{IMAGE_SOURCES['WIKIMEDIA']['search_endpoint'].format(query=f'{brand} car logo')}"
        try:
            response = self._make_request(wiki_url)
            results = response.get('query', {}).get('search', [])
            if results:
                image_title = results[0]['title']
                image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{image_title}"
                if self._download_and_save_image(image_url, save_path):
                    return save_path
        except Exception as e:
            print(f"Erreur lors de la recherche Wikimedia pour {brand}: {str(e)}")
        
        return None

    def download_vehicle_images(self, make: str, model: str, year: int) -> List[str]:
        """Télécharge les images d'un véhicule spécifique."""
        search_query = f"{make} {model} {year}"
        saved_images = []
        
        # Chercher sur Wikimedia
        wiki_url = f"{IMAGE_SOURCES['WIKIMEDIA']['base_url']}{IMAGE_SOURCES['WIKIMEDIA']['search_endpoint'].format(query=search_query)}"
        
        try:
            response = self._make_request(wiki_url)
            results = response.get('query', {}).get('search', [])
            
            for result in results[:5]:  # Limiter à 5 images par modèle
                image_title = result['title']
                image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{image_title}"
                
                # Créer un nom de fichier unique
                file_hash = hashlib.md5(f"{make}{model}{year}{image_url}".encode()).hexdigest()[:10]
                save_path = os.path.join(
                    self.save_dir, 
                    'vehicles', 
                    make.lower(),
                    f"{model.lower()}_{year}_{file_hash}.jpg"
                )
                
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                if self._download_and_save_image(image_url, save_path):
                    saved_images.append(save_path)
        
        except Exception as e:
            print(f"Erreur lors de la recherche d'images pour {search_query}: {str(e)}")
        
        return saved_images

    def _make_request(self, url: str) -> Dict:
        """Effectue une requête HTTP avec gestion des erreurs et rate limiting."""
        try:
            time.sleep(self.rate_limit_delay)
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erreur lors de la requête à {url}: {str(e)}")
            return {}

    def _download_and_save_image(self, url: str, save_path: str, min_size: int = 1000) -> bool:
        """Télécharge et sauvegarde une image avec validation."""
        try:
            response = self.session.get(url, stream=True)
            if response.status_code != 200:
                return False

            # Vérifier la taille du fichier
            content = response.content
            if len(content) < min_size:
                return False

            # Ouvrir et valider l'image
            img = Image.open(io.BytesIO(content))
            
            # Vérifier les dimensions minimales
            if img.width < 100 or img.height < 100:
                return False

            # Convertir en RGB si nécessaire
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Redimensionner si trop grande
            max_size = (1920, 1080)
            if img.width > max_size[0] or img.height > max_size[1]:
                img.thumbnail(max_size, Image.LANCZOS)

            # Sauvegarder avec optimisation
            img.save(save_path, 'JPEG', quality=85, optimize=True)
            return True

        except Exception as e:
            print(f"Erreur lors du téléchargement de {url}: {str(e)}")
            return False

    def generate_color_swatches(self, colors: Dict[str, str]) -> Dict[str, str]:
        """Génère des échantillons de couleurs."""
        color_paths = {}
        
        for color_name, hex_code in colors.items():
            try:
                # Créer une image de couleur unie
                img = Image.new('RGB', (200, 200), hex_code)
                
                # Sauvegarder l'échantillon
                save_path = os.path.join(self.save_dir, 'colors', f"{color_name.lower()}.png")
                img.save(save_path, 'PNG')
                
                color_paths[color_name] = save_path
                
            except Exception as e:
                print(f"Erreur lors de la création de l'échantillon pour {color_name}: {str(e)}")
        
        return color_paths
