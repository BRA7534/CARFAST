import base64
import os
from cryptography.fernet import Fernet
from pathlib import Path

# Génération d'une clé de chiffrement
def generate_key():
    return Fernet.generate_key()

# Chiffrement du fichier
def encrypt_file(key, input_file, output_file):
    f = Fernet(key)
    
    with open(input_file, 'rb') as file:
        file_data = file.read()
    
    encrypted_data = f.encrypt(file_data)
    
    with open(output_file, 'wb') as file:
        file.write(encrypted_data)

def main():
    # Création du dossier secrets s'il n'existe pas
    secrets_dir = Path("../secrets")
    secrets_dir.mkdir(exist_ok=True)
    
    # Génération de la clé
    key = generate_key()
    
    # Sauvegarde de la clé
    with open(secrets_dir / "encryption.key", "wb") as key_file:
        key_file.write(key)
    
    # Chiffrement du keystore.properties
    encrypt_file(
        key,
        "../androidApp/keystore.properties",
        secrets_dir / "keystore.properties.encrypted"
    )
    
    # Chiffrement du keystore
    encrypt_file(
        key,
        "../androidApp/production-keystore.jks",
        secrets_dir / "production-keystore.jks.encrypted"
    )
    
    print("Fichiers chiffrés avec succès!")
    print("IMPORTANT: Sauvegardez le fichier encryption.key dans un endroit sûr!")
    print("Les fichiers chiffrés se trouvent dans le dossier 'secrets'")

if __name__ == "__main__":
    main()
