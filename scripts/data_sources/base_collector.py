"""
Classe de base pour les collecteurs de données
"""

from typing import Dict, Any, List
from .data import (
    ALL_BRANDS,
    BODY_TYPES,
    ENGINE_TYPES,
    TRIM_LEVELS,
    AVAILABLE_OPTIONS,
    AVAILABLE_COLORS
)

class BaseCollector:
    def __init__(self):
        self.brands_data = ALL_BRANDS
        self.body_types = BODY_TYPES
        self.engine_types = ENGINE_TYPES
        self.trim_levels = TRIM_LEVELS
        self.available_options = AVAILABLE_OPTIONS
        self.available_colors = AVAILABLE_COLORS

    def _get_available_engines(self, brand: str, model: str) -> List[Dict[str, Any]]:
        """Génère la liste des motorisations disponibles pour une marque et un modèle spécifiques."""
        engines = []
        model_lower = model.lower()
        
        # Déterminer la gamme du véhicule
        if any(lux in model_lower for lux in ['série 7', 's-class', 'a8', 'ls']):
            vehicle_class = 'luxury'
        elif any(mid in model_lower for mid in ['série 5', 'e-class', 'a6', 'camry']):
            vehicle_class = 'mid'
        else:
            vehicle_class = 'compact'
            
        # Déterminer le type de véhicule
        if any(suv in model_lower for suv in ['suv', 'crossover', 'x', 'q', 'glc', 'rav']):
            vehicle_type = 'suv'
        else:
            vehicle_type = 'car'
            
        # Déterminer les types de moteurs disponibles
        if 'e-' in model_lower or 'ë-' in model_lower or brand == 'Tesla':
            engine_types = ['Électrique']
        elif brand in ['BMW', 'Mercedes', 'Audi'] and vehicle_class in ['luxury', 'mid']:
            engine_types = ['Essence', 'Diesel', 'Hybride Rechargeable']
        elif brand in ['Toyota', 'Honda']:
            engine_types = ['Essence', 'Hybride']
        else:
            engine_types = ['Essence', 'Diesel']
            
        # Générer les motorisations appropriées
        for engine_type in engine_types:
            if engine_type == 'Essence':
                # Sélectionner une seule cylindrée appropriée
                if vehicle_class == 'luxury':
                    displacement = 2998
                    powers = [300, 350]
                elif vehicle_class == 'mid':
                    displacement = 1984
                    powers = [180, 250]
                else:
                    displacement = 1332
                    powers = [110, 130]
                    
                for power in powers:
                    engines.append({
                        'type': engine_type,
                        'power': power,
                        'displacement': displacement
                    })
                    
            elif engine_type == 'Diesel':
                # Sélectionner une seule cylindrée appropriée
                if vehicle_class == 'luxury':
                    displacement = 2993
                    powers = [300, 350]
                elif vehicle_class == 'mid':
                    displacement = 1995
                    powers = [180, 250]
                else:
                    displacement = 1461
                    powers = [90, 110]
                    
                for power in powers:
                    engines.append({
                        'type': engine_type,
                        'power': power,
                        'displacement': displacement
                    })
                    
            elif engine_type == 'Hybride':
                # Une seule version hybride par modèle
                if vehicle_class == 'luxury':
                    power = 180
                else:
                    power = 140
                    
                engines.append({
                    'type': engine_type,
                    'power': power,
                    'hybrid_type': 'HEV'
                })
                
            elif engine_type == 'Hybride Rechargeable':
                # Une seule version PHEV par modèle
                if vehicle_class == 'luxury':
                    power = 300
                else:
                    power = 225
                    
                engines.append({
                    'type': engine_type,
                    'power': power,
                    'hybrid_type': 'PHEV'
                })
                
            elif engine_type == 'Électrique':
                # Une ou deux versions selon le type
                if vehicle_type == 'suv':
                    if vehicle_class == 'luxury':
                        powers = [400, 500]
                        battery = 100
                    else:
                        powers = [300, 400]
                        battery = 77
                else:
                    if vehicle_class == 'luxury':
                        powers = [400]
                        battery = 100
                    else:
                        powers = [170]
                        battery = 60
                        
                for power in powers:
                    engines.append({
                        'type': engine_type,
                        'power': power,
                        'battery': battery
                    })
        
        return engines

    def _get_trim_levels(self, brand: str) -> List[Dict[str, Any]]:
        """Génère la liste des niveaux de finition pour une marque spécifique."""
        trims = []
        
        # Adapter les niveaux de finition selon la marque
        if brand in ['BMW', 'Mercedes', 'Audi']:
            categories = ['Premium']
            levels = self.trim_levels['Premium'][:2]  # Maximum 2 finitions premium
        elif brand == 'DS':
            categories = ['Premium']
            levels = self.trim_levels['Premium'][:1]  # Une seule finition premium
        else:
            categories = ['Entrée de gamme', 'Milieu de gamme']
            levels = []
            for category in categories:
                levels.extend(self.trim_levels[category][:1])  # Une finition par catégorie
            
        for level in levels:
            trims.append({
                'category': categories[0],  # Utiliser la première catégorie
                'name': level
            })
        
        return trims

    def _get_available_options(self) -> Dict[str, List[str]]:
        """Retourne la liste des options disponibles."""
        # Limiter à 3 options par catégorie
        limited_options = {}
        for category, options in self.available_options.items():
            limited_options[category] = options[:3]
        return limited_options

    def _get_available_colors(self) -> Dict[str, Dict[str, str]]:
        """Retourne la liste des couleurs disponibles."""
        # Limiter à 5 couleurs par modèle
        standard_colors = ['Blanc Nacré', 'Noir Étoilé', 'Gris Titanium', 'Bleu Iron', 'Rouge Flamme']
        limited_colors = {}
        for color in standard_colors:
            if color in self.available_colors:
                limited_colors[color] = self.available_colors[color]
        return limited_colors
