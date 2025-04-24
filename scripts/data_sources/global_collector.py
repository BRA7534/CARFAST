"""
Collecteur de données pour les marques mondiales
"""

from typing import Dict, Any, List
from .base_collector import BaseCollector
from .data import (
    ALL_BRANDS,
    BODY_TYPES,
    ENGINE_TYPES,
    TRIM_LEVELS,
    AVAILABLE_OPTIONS,
    AVAILABLE_COLORS
)

class GlobalCollector(BaseCollector):
    def __init__(self):
        self.brands_data = ALL_BRANDS
        self.body_types = BODY_TYPES
        self.engine_types = ENGINE_TYPES
        self.trim_levels = TRIM_LEVELS
        self.available_options = AVAILABLE_OPTIONS
        self.available_colors = AVAILABLE_COLORS

    def collect_full_data(self, start_year: int, end_year: int) -> Dict[str, Any]:
        """Collecte toutes les données pour les marques mondiales."""
        full_data = {
            'makes': {},
            'models': {},
            'types': {},
            'specs': {}
        }

        # Pour chaque marque
        for brand, brand_data in self.brands_data.items():
            if brand in ['Renault', 'Peugeot', 'Citroën', 'DS']:  # Skip French brands
                continue
                
            print(f"Collecte des données pour {brand}...")
            
            # Informations de la marque
            full_data['makes'][brand] = {
                'name': brand,
                'country': brand_data['country'],
                'logo_url': f"https://www.carlogos.org/car-logos/{brand.lower()}-logo.png"
            }

            full_data['models'][brand] = {}
            
            # Pour chaque année
            for year in range(start_year, end_year + 1):
                if year in brand_data['models_by_year']:
                    full_data['models'][brand][year] = {}
                    
                    # Pour chaque modèle
                    for model in brand_data['models_by_year'][year]:
                        model_full_name = f"{brand} {model}"
                        
                        # Trouver le type de carrosserie
                        body_type = None
                        for type_name, models in self.body_types.items():
                            if model_full_name in models:
                                body_type = type_name
                                break
                        
                        # Créer les spécifications du modèle
                        model_specs = {
                            'name': model,
                            'brand': brand,
                            'year': year,
                            'body_type': body_type,
                            'engine_types': self._get_available_engines(brand, model),
                            'trim_levels': self._get_trim_levels(brand),
                            'options': self._get_available_options(),
                            'colors': self._get_available_colors()
                        }
                        
                        full_data['models'][brand][year][model] = model_specs
                        
                        # Ajouter aux spécifications générales
                        if brand not in full_data['specs']:
                            full_data['specs'][brand] = {}
                        if year not in full_data['specs'][brand]:
                            full_data['specs'][brand][year] = {}
                        
                        full_data['specs'][brand][year][model] = model_specs

        return full_data

    def _get_available_engines(self, brand: str, model: str) -> List[Dict[str, Any]]:
        """Génère la liste des motorisations disponibles pour une marque et un modèle spécifiques."""
        engines = []
        
        # Déterminer les types de moteurs disponibles en fonction de la marque et du modèle
        if brand in ['BMW', 'Mercedes', 'Audi']:
            engine_types = ['Essence', 'Diesel', 'Hybride Rechargeable', 'Électrique']
        elif brand in ['Toyota', 'Honda']:
            engine_types = ['Essence', 'Hybride']
        elif brand == 'Tesla':
            engine_types = ['Électrique']
        else:
            engine_types = ['Essence', 'Diesel', 'Hybride']
            
        for engine_type in engine_types:
            if engine_type == 'Essence':
                for power in self.engine_types[engine_type]['puissances']:
                    for displacement in self.engine_types[engine_type]['cylindrees']:
                        engines.append({
                            'type': engine_type,
                            'power': power,
                            'displacement': displacement
                        })
            elif engine_type == 'Diesel':
                for power in self.engine_types[engine_type]['puissances']:
                    for displacement in self.engine_types[engine_type]['cylindrees']:
                        engines.append({
                            'type': engine_type,
                            'power': power,
                            'displacement': displacement
                        })
            elif engine_type in ['Hybride', 'Hybride Rechargeable']:
                for power in self.engine_types[engine_type]['puissances']:
                    for hybrid_type in self.engine_types[engine_type]['types']:
                        engines.append({
                            'type': engine_type,
                            'power': power,
                            'hybrid_type': hybrid_type
                        })
            elif engine_type == 'Électrique':
                for power in self.engine_types[engine_type]['puissances']:
                    for battery in self.engine_types[engine_type]['batteries']:
                        engines.append({
                            'type': engine_type,
                            'power': power,
                            'battery': battery
                        })
        
        return engines

    def _get_trim_levels(self, brand: str) -> List[Dict[str, Any]]:
        """Génère la liste des niveaux de finition pour une marque spécifique."""
        trims = []
        
        # Adapter les niveaux de finition en fonction de la marque
        if brand in ['BMW', 'Mercedes', 'Audi']:
            categories = ['Premium', 'Sport']
        else:
            categories = ['Entrée de gamme', 'Milieu de gamme', 'Haut de gamme']
            
        for category in categories:
            for level in self.trim_levels[category]:
                trims.append({
                    'category': category,
                    'name': level
                })
        
        return trims

    def _get_available_options(self) -> Dict[str, List[str]]:
        """Retourne la liste des options disponibles."""
        return self.available_options

    def _get_available_colors(self) -> Dict[str, Dict[str, str]]:
        """Retourne la liste des couleurs disponibles."""
        return self.available_colors
