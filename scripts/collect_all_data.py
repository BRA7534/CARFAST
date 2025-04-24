"""
Script principal de collecte de données
"""

import json
import sqlite3
from pathlib import Path
from data_sources.french_collector import FrenchCollector
from data_sources.global_collector import GlobalCollector
from data_sources.reviews_collector import ReviewsCollector

def collect_and_save_data(start_year: int = 2015, end_year: int = 2024):
    """Collecte et sauvegarde toutes les données des véhicules."""
    
    # Créer les collecteurs
    french_collector = FrenchCollector()
    global_collector = GlobalCollector()
    reviews_collector = ReviewsCollector()
    
    # Collecter les données
    print("Collecte des données des marques françaises...")
    french_data = french_collector.collect_full_data(start_year, end_year)
    
    print("\nCollecte des données des marques mondiales...")
    global_data = global_collector.collect_full_data(start_year, end_year)
    
    # Fusionner les données
    all_data = {
        'makes': {**french_data['makes'], **global_data['makes']},
        'models': {**french_data['models'], **global_data['models']},
        'types': {**french_data.get('types', {}), **global_data.get('types', {})},
        'specs': {**french_data['specs'], **global_data['specs']}
    }
    
    # Créer le dossier de sortie s'il n'existe pas
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Sauvegarder en JSON
    json_path = output_dir / 'vehicle_data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"\nDonnées sauvegardées dans {json_path}")
    
    # Sauvegarder en SQLite
    db_path = output_dir / 'vehicle_data.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Créer les tables avec des contraintes
    cursor.execute('''DROP TABLE IF EXISTS makes''')
    cursor.execute('''DROP TABLE IF EXISTS models''')
    cursor.execute('''DROP TABLE IF EXISTS engine_types''')
    cursor.execute('''DROP TABLE IF EXISTS trim_levels''')
    cursor.execute('''DROP TABLE IF EXISTS reviews''')
    
    cursor.execute('''
    CREATE TABLE makes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        country TEXT NOT NULL,
        logo_url TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE models (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make_id INTEGER,
        name TEXT NOT NULL,
        year INTEGER NOT NULL,
        body_type TEXT,
        FOREIGN KEY (make_id) REFERENCES makes (id),
        UNIQUE(make_id, name, year)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE engine_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id INTEGER,
        type TEXT NOT NULL,
        power INTEGER,
        displacement INTEGER,
        hybrid_type TEXT,
        battery_capacity INTEGER,
        FOREIGN KEY (model_id) REFERENCES models (id),
        UNIQUE(model_id, type, power, displacement, hybrid_type, battery_capacity)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE trim_levels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id INTEGER,
        category TEXT NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (model_id) REFERENCES models (id),
        UNIQUE(model_id, category, name)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id INTEGER,
        rating REAL,
        review TEXT,
        FOREIGN KEY (model_id) REFERENCES models (id)
    )
    ''')
    
    # Insérer les données avec gestion des doublons
    for brand, brand_data in all_data['makes'].items():
        try:
            cursor.execute(
                'INSERT OR IGNORE INTO makes (name, country, logo_url) VALUES (?, ?, ?)',
                (brand, brand_data['country'], brand_data['logo_url'])
            )
            make_id = cursor.lastrowid or cursor.execute(
                'SELECT id FROM makes WHERE name = ?', (brand,)
            ).fetchone()[0]
            
            for year, year_data in all_data['models'][brand].items():
                for model, model_data in year_data.items():
                    try:
                        cursor.execute(
                            'INSERT OR IGNORE INTO models (make_id, name, year, body_type) VALUES (?, ?, ?, ?)',
                            (make_id, model, year, model_data['body_type'])
                        )
                        model_id = cursor.lastrowid or cursor.execute(
                            'SELECT id FROM models WHERE make_id = ? AND name = ? AND year = ?',
                            (make_id, model, year)
                        ).fetchone()[0]
                        
                        # Ajouter les motorisations
                        for engine in model_data['engine_types']:
                            try:
                                cursor.execute(
                                    '''INSERT OR IGNORE INTO engine_types 
                                    (model_id, type, power, displacement, hybrid_type, battery_capacity)
                                    VALUES (?, ?, ?, ?, ?, ?)''',
                                    (
                                        model_id,
                                        engine['type'],
                                        engine.get('power'),
                                        engine.get('displacement'),
                                        engine.get('hybrid_type'),
                                        engine.get('battery')
                                    )
                                )
                            except sqlite3.Error as e:
                                print(f"Erreur lors de l'ajout de la motorisation pour {brand} {model} {year}: {e}")
                        
                        # Ajouter les niveaux de finition
                        for trim in model_data['trim_levels']:
                            try:
                                cursor.execute(
                                    'INSERT OR IGNORE INTO trim_levels (model_id, category, name) VALUES (?, ?, ?)',
                                    (model_id, trim['category'], trim['name'])
                                )
                            except sqlite3.Error as e:
                                print(f"Erreur lors de l'ajout de la finition pour {brand} {model} {year}: {e}")
                        
                        # Collecter et sauvegarder les avis
                        print(f"\nCollecte des avis pour {brand} {model} {year}...")
                        reviews = reviews_collector.collect_reviews(brand, model, year)
                        if reviews:
                            for review in reviews:
                                try:
                                    cursor.execute(
                                        'INSERT INTO reviews (model_id, rating, review) VALUES (?, ?, ?)',
                                        (model_id, review['rating'], review['review'])
                                    )
                                except sqlite3.Error as e:
                                    print(f"Erreur lors de l'ajout de l'avis pour {brand} {model} {year}: {e}")
                                
                    except sqlite3.Error as e:
                        print(f"Erreur lors de l'ajout du modèle {brand} {model} {year}: {e}")
                        
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout de la marque {brand}: {e}")
    
    # Créer des index pour améliorer les performances
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_models_make ON models(make_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_engine_model ON engine_types(model_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_trim_model ON trim_levels(model_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reviews_model ON reviews(model_id)')
    
    conn.commit()
    conn.close()
    print(f"Données sauvegardées dans {db_path}")

if __name__ == '__main__':
    collect_and_save_data()
