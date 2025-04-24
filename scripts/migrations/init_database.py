"""
Script d'initialisation de la base de données
"""

import sqlite3
import os

def init_database():
    """Initialise la base de données avec les tables nécessaires."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database/vehicle_database.db')
    
    # Créer le dossier database s'il n'existe pas
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Supprimer la base de données si elle existe déjà
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Créer une nouvelle connexion
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Créer la table des marques
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS brands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                logo_url TEXT
            )
        """)
        
        # Créer la table des modèles
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                year INTEGER NOT NULL,
                FOREIGN KEY (brand_id) REFERENCES brands(id),
                UNIQUE(brand_id, name, year)
            )
        """)
        
        # Créer la table des spécifications techniques
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS technical_specs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id INTEGER NOT NULL,
                engine_type TEXT,
                power INTEGER,
                displacement INTEGER,
                battery_capacity INTEGER,
                hybrid_type TEXT,
                FOREIGN KEY (model_id) REFERENCES models(id)
            )
        """)
        
        # Créer la table des couleurs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS colors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                hex_code TEXT NOT NULL,
                type TEXT NOT NULL,
                UNIQUE(name, hex_code)
            )
        """)
        
        # Créer la table de liaison modèles-couleurs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_colors (
                model_id INTEGER NOT NULL,
                color_id INTEGER NOT NULL,
                FOREIGN KEY (model_id) REFERENCES models(id),
                FOREIGN KEY (color_id) REFERENCES colors(id),
                PRIMARY KEY (model_id, color_id)
            )
        """)
        
        # Créer la table des options
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                UNIQUE(name, category)
            )
        """)
        
        # Créer la table de liaison modèles-options
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_options (
                model_id INTEGER NOT NULL,
                option_id INTEGER NOT NULL,
                FOREIGN KEY (model_id) REFERENCES models(id),
                FOREIGN KEY (option_id) REFERENCES options(id),
                PRIMARY KEY (model_id, option_id)
            )
        """)
        
        conn.commit()
        print("Base de données initialisée avec succès !")
        
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'initialisation de la base de données : {str(e)}")
        raise e
        
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()
