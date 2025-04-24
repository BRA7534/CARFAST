import sqlite3
import os

def setup_database():
    """Configure la base de données avec le schéma initial."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'shared/src/commonMain/resources/database/catalog.db')
    migrations_dir = os.path.join(base_dir, 'shared/src/commonMain/resources/database/migrations')

    # Créer le dossier de la base de données s'il n'existe pas
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Exécuter les migrations dans l'ordre
        for migration_file in sorted(os.listdir(migrations_dir)):
            if migration_file.endswith('.sql'):
                print(f"Exécution de la migration : {migration_file}")
                with open(os.path.join(migrations_dir, migration_file), 'r', encoding='utf-8') as f:
                    sql = f.read()
                    cursor.executescript(sql)
        
        conn.commit()
        print("Base de données configurée avec succès !")
        
    except Exception as e:
        print(f"Erreur lors de la configuration de la base de données : {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    setup_database()
