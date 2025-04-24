import os
import cairosvg
from PIL import Image

# Tailles pour Android (en dp)
ANDROID_SIZES = {
    'mdpi': 48,    # 1x
    'hdpi': 72,    # 1.5x
    'xhdpi': 96,   # 2x
    'xxhdpi': 144, # 3x
    'xxxhdpi': 192 # 4x
}

# Tailles pour iOS
IOS_SIZES = {
    '1x': 60,
    '2x': 120,
    '3x': 180
}

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_android_icons(svg_path):
    base_dir = 'androidApp/src/main/res'
    
    for density, size in ANDROID_SIZES.items():
        # Créer le dossier de ressources
        res_dir = os.path.join(base_dir, f'mipmap-{density}')
        ensure_dir(res_dir)
        
        # Générer l'icône
        output_path = os.path.join(res_dir, 'ic_launcher.png')
        cairosvg.svg2png(
            url=svg_path,
            write_to=output_path,
            output_width=size,
            output_height=size
        )
        
        # Optimiser l'image
        img = Image.open(output_path)
        img.save(output_path, optimize=True, quality=95)

def generate_ios_icons(svg_path):
    base_dir = 'iosApp/CarFast/Assets.xcassets/AppIcon.appiconset'
    ensure_dir(base_dir)
    
    for scale, size in IOS_SIZES.items():
        output_path = os.path.join(base_dir, f'logo_{scale}.png')
        cairosvg.svg2png(
            url=svg_path,
            write_to=output_path,
            output_width=size,
            output_height=size
        )
        
        # Optimiser l'image
        img = Image.open(output_path)
        img.save(output_path, optimize=True, quality=95)

def generate_all_assets():
    svg_path = 'shared/src/commonMain/resources/assets/logo/logo.svg'
    
    print("Génération des icônes Android...")
    generate_android_icons(svg_path)
    
    print("Génération des icônes iOS...")
    generate_ios_icons(svg_path)
    
    print("Génération terminée !")

if __name__ == '__main__':
    generate_all_assets()
