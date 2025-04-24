import base64
from cryptography.fernet import Fernet
from pathlib import Path

def decrypt_file(key, input_file, output_file):
    f = Fernet(key)
    
    with open(input_file, 'rb') as file:
        encrypted_data = file.read()
    
    decrypted_data = f.decrypt(encrypted_data)
    
    with open(output_file, 'wb') as file:
        file.write(decrypted_data)

def main():
    secrets_dir = Path("../secrets")
    
    # Lecture de la clé
    try:
        with open(secrets_dir / "encryption.key", "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        print("ERREUR: Fichier de clé non trouvé!")
        return
    
    # Déchiffrement du keystore.properties
    decrypt_file(
        key,
        secrets_dir / "keystore.properties.encrypted",
        "../androidApp/keystore.properties"
    )
    
    # Déchiffrement du keystore
    decrypt_file(
        key,
        secrets_dir / "production-keystore.jks.encrypted",
        "../androidApp/production-keystore.jks"
    )
    
    print("Fichiers déchiffrés avec succès!")

if __name__ == "__main__":
    main()
