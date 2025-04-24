import os
import shutil
from PIL import Image
import json

class AssetImporter:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = os.path.join(self.project_root, 'shared', 'src', 'commonMain', 'resources', 'assets')
        
        # Créer les dossiers nécessaires
        self.brand_logos_dir = os.path.join(self.assets_dir, 'brands')
        self.vehicles_dir = os.path.join(self.assets_dir, 'vehicles')
        self.thumbnails_dir = os.path.join(self.assets_dir, 'thumbnails')
        
        for directory in [self.brand_logos_dir, self.vehicles_dir, self.thumbnails_dir]:
            os.makedirs(directory, exist_ok=True)

    def optimize_image(self, image_path, max_size=(800, 800), quality=85):
        """Optimise une image pour l'utilisation dans l'application."""
        with Image.open(image_path) as img:
            # Convertir en RGB si nécessaire
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Redimensionner si nécessaire
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.LANCZOS)
            
            # Sauvegarder avec optimisation
            output_path = image_path.rsplit('.', 1)[0] + '.jpg'
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            return output_path

    def create_thumbnail(self, image_path, size=(200, 200)):
        """Crée une miniature d'une image."""
        thumbnail_name = os.path.basename(image_path)
        thumbnail_path = os.path.join(self.thumbnails_dir, thumbnail_name)
        
        with Image.open(image_path) as img:
            img.thumbnail(size, Image.LANCZOS)
            img.save(thumbnail_path, 'JPEG', quality=75, optimize=True)
        
        return thumbnail_path

    def import_brand_logos(self, source_dir):
        """Importe les logos des marques."""
        print("Importation des logos des marques...")
        brand_mapping = {}
        
        for filename in os.listdir(source_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.svg')):
                source_path = os.path.join(source_dir, filename)
                brand_name = os.path.splitext(filename)[0].lower()
                
                # Destination dans le projet
                dest_path = os.path.join(self.brand_logos_dir, f"{brand_name}.jpg")
                
                # Optimiser et copier le logo
                optimized_path = self.optimize_image(source_path, max_size=(400, 400))
                shutil.copy2(optimized_path, dest_path)
                
                brand_mapping[brand_name] = f"assets/brands/{brand_name}.jpg"
                print(f"Logo importé : {brand_name}")
        
        # Sauvegarder le mapping des logos
        with open(os.path.join(self.assets_dir, 'brand_logos.json'), 'w') as f:
            json.dump(brand_mapping, f, indent=2)

    def import_vehicle_photos(self, source_dir):
        """Importe les photos des véhicules."""
        print("Importation des photos de véhicules...")
        vehicle_mapping = {}
        
        for root, _, files in os.walk(source_dir):
            for filename in files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    source_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(root, source_dir)
                    vehicle_id = os.path.splitext(filename)[0]
                    
                    # Créer le dossier de destination si nécessaire
                    dest_dir = os.path.join(self.vehicles_dir, relative_path)
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    # Destination dans le projet
                    dest_path = os.path.join(dest_dir, f"{vehicle_id}.jpg")
                    
                    # Optimiser et copier la photo
                    optimized_path = self.optimize_image(source_path)
                    shutil.copy2(optimized_path, dest_path)
                    
                    # Créer une miniature
                    thumbnail_path = self.create_thumbnail(optimized_path)
                    
                    # Enregistrer les chemins dans le mapping
                    vehicle_mapping[vehicle_id] = {
                        'photo': f"assets/vehicles/{relative_path}/{vehicle_id}.jpg",
                        'thumbnail': f"assets/thumbnails/{os.path.basename(thumbnail_path)}"
                    }
                    print(f"Photo importée : {vehicle_id}")
        
        # Sauvegarder le mapping des photos
        with open(os.path.join(self.assets_dir, 'vehicle_photos.json'), 'w') as f:
            json.dump(vehicle_mapping, f, indent=2)

def main():
    importer = AssetImporter()
    
    # Demander les chemins source
    brand_logos_source = input("Chemin vers le dossier des logos de marques : ").strip()
    vehicle_photos_source = input("Chemin vers le dossier des photos de véhicules : ").strip()
    
    if os.path.exists(brand_logos_source):
        importer.import_brand_logos(brand_logos_source)
    else:
        print("Dossier des logos introuvable !")
        
    if os.path.exists(vehicle_photos_source):
        importer.import_vehicle_photos(vehicle_photos_source)
    else:
        print("Dossier des photos introuvable !")
    
    print("Importation terminée !")

if __name__ == '__main__':
    main()
