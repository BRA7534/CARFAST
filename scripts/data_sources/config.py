"""
Configuration et données statiques pour les collecteurs de données
"""

from .data import (
    ALL_BRANDS,
    BODY_TYPES,
    ENGINE_TYPES,
    TRIM_LEVELS,
    AVAILABLE_OPTIONS,
    AVAILABLE_COLORS
)

# Marques françaises
FRENCH_BRANDS_DATA = {
    'Renault': {
        'models': {
            2023: ['Clio', 'Captur', 'Arkana', 'Megane E-Tech', 'Austral'],
            2024: ['Clio', 'Captur', 'Arkana', 'Megane E-Tech', 'Austral', 'Scenic E-Tech']
        }
    },
    'Peugeot': {
        'models': {
            2023: ['208', '2008', '308', '3008', '408', '508'],
            2024: ['208', '2008', '308', '3008', '408', '508', 'E-3008']
        }
    },
    'Citroën': {
        'models': {
            2023: ['C3', 'C3 Aircross', 'C4', 'C5 X', 'C5 Aircross'],
            2024: ['C3', 'C3 Aircross', 'C4', 'C5 X', 'C5 Aircross', 'ë-C3']
        }
    },
    'DS': {
        'models': {
            2023: ['DS 3', 'DS 4', 'DS 7', 'DS 9'],
            2024: ['DS 3', 'DS 4', 'DS 7', 'DS 9']
        }
    }
}

# Marques mondiales
GLOBAL_BRANDS_DATA = {
    'Toyota': {
        'country': 'Japon',
        'models': {
            2023: ['Yaris', 'Corolla', 'RAV4', 'C-HR', 'Camry', 'Highlander'],
            2024: ['Yaris', 'Corolla', 'RAV4', 'C-HR', 'Camry', 'Highlander', 'bZ4X']
        },
        'engines': {
            'Yaris': {
                'Essence': {'puissances': [70, 90], 'cylindrees': [998, 1496]},
                'Hybride': {'puissances': [116], 'types': ['HEV']}
            },
            'Corolla': {
                'Hybride': {'puissances': [140, 196], 'types': ['HEV']}
            }
        }
    },
    'Volkswagen': {
        'country': 'Allemagne',
        'models': {
            2023: ['Polo', 'Golf', 'T-Roc', 'Tiguan', 'ID.3', 'ID.4', 'ID.5'],
            2024: ['Polo', 'Golf', 'T-Roc', 'Tiguan', 'ID.3', 'ID.4', 'ID.5', 'ID.7']
        },
        'engines': {
            'Golf': {
                'Essence': {'puissances': [110, 130, 150], 'cylindrees': [1498, 1984]},
                'Hybride Rechargeable': {'puissances': [204, 245], 'types': ['PHEV']}
            }
        }
    },
    'BMW': {
        'country': 'Allemagne',
        'models': {
            2023: ['Série 1', 'Série 2', 'Série 3', 'Série 4', 'X1', 'X3', 'iX1', 'i4'],
            2024: ['Série 1', 'Série 2', 'Série 3', 'Série 4', 'X1', 'X3', 'iX1', 'i4', 'i5']
        },
        'engines': {
            'Série 3': {
                'Essence': {'puissances': [184, 245, 374], 'cylindrees': [1998, 2998]},
                'Diesel': {'puissances': [150, 190, 286], 'cylindrees': [1995, 2993]},
                'Hybride Rechargeable': {'puissances': [292, 394], 'types': ['PHEV']}
            }
        }
    },
    'Mercedes': {
        'country': 'Allemagne',
        'models': {
            2023: ['Classe A', 'Classe C', 'Classe E', 'GLA', 'GLB', 'GLC', 'EQA', 'EQB', 'EQC'],
            2024: ['Classe A', 'Classe C', 'Classe E', 'GLA', 'GLB', 'GLC', 'EQA', 'EQB', 'EQC', 'EQE']
        },
        'engines': {
            'Classe C': {
                'Essence': {'puissances': [170, 204, 258], 'cylindrees': [1496, 1999]},
                'Diesel': {'puissances': [163, 200, 265], 'cylindrees': [1993, 2925]},
                'Hybride Rechargeable': {'puissances': [313, 381], 'types': ['PHEV']}
            }
        }
    }
}

# Types de carrosserie
BODY_TYPES = {
    'Berline': ['Renault Megane', 'Peugeot 308', 'BMW Série 3', 'Mercedes Classe C'],
    'SUV': ['Renault Captur', 'Peugeot 3008', 'BMW X3', 'Mercedes GLC'],
    'Compacte': ['Renault Clio', 'Peugeot 208', 'BMW Série 1', 'Mercedes Classe A'],
    'Break': ['Peugeot 308 SW', 'BMW Série 3 Touring', 'Mercedes Classe C Break'],
    'Coupé': ['BMW Série 4', 'Mercedes Classe C Coupé'],
    'Crossover': ['Renault Arkana', 'Toyota C-HR', 'Volkswagen T-Roc']
}

# Types de moteurs
ENGINE_TYPES = {
    'Essence': {
        'puissances': [70, 90, 110, 130, 150, 180, 200],
        'cylindrees': [998, 1199, 1332, 1498, 1984, 2998]
    },
    'Diesel': {
        'puissances': [90, 110, 130, 150, 180, 200],
        'cylindrees': [1461, 1498, 1995, 2993]
    },
    'Hybride': {
        'puissances': [140, 160, 180, 200, 225],
        'types': ['HEV', 'MHEV']
    },
    'Hybride Rechargeable': {
        'puissances': [180, 225, 300, 360],
        'types': ['PHEV']
    },
    'Électrique': {
        'puissances': [136, 150, 170, 204, 245, 300, 408],
        'batteries': [40, 50, 60, 77, 82, 100]
    }
}

# Niveaux de finition
TRIM_LEVELS = {
    'Base': ['Life', 'Active', 'Première', 'Business'],
    'Milieu de gamme': ['Zen', 'Allure', 'Avantage', 'Style'],
    'Haut de gamme': ['Intens', 'GT Line', 'RS Line', 'Executive'],
    'Premium': ['Iconic', 'GT', 'Performance Line+', 'AMG Line']
}

# Options disponibles
AVAILABLE_OPTIONS = {
    'Confort': [
        'Climatisation automatique bi-zone',
        'Sièges chauffants',
        'Sièges ventilés',
        'Toit ouvrant panoramique',
        'Accès et démarrage mains libres'
    ],
    'Sécurité': [
        'Régulateur adaptatif',
        'Freinage automatique d\'urgence',
        'Surveillance des angles morts',
        'Aide au maintien dans la voie',
        'Vision tête haute'
    ],
    'Multimédia': [
        'Navigation connectée',
        'Système audio premium',
        'Chargeur smartphone à induction',
        'Apple CarPlay / Android Auto',
        'Écran tactile 10"'
    ],
    'Design': [
        'Jantes alliage',
        'Vitres surteintées',
        'Peinture métallisée',
        'Pack Sport',
        'Sellerie cuir'
    ]
}

# Couleurs disponibles
AVAILABLE_COLORS = {
    'Blanc Nacré': {'name': 'Blanc Nacré', 'hex': '#FFFFFF', 'type': 'Nacré'},
    'Noir Étoilé': {'name': 'Noir Étoilé', 'hex': '#000000', 'type': 'Métallisé'},
    'Gris Titanium': {'name': 'Gris Titanium', 'hex': '#848484', 'type': 'Métallisé'},
    'Bleu Iron': {'name': 'Bleu Iron', 'hex': '#2B4F81', 'type': 'Métallisé'},
    'Rouge Flamme': {'name': 'Rouge Flamme', 'hex': '#CF1020', 'type': 'Métallisé'},
    'Vert Olive': {'name': 'Vert Olive', 'hex': '#3D4F25', 'type': 'Métallisé'},
    'Orange Valencia': {'name': 'Orange Valencia', 'hex': '#F47B00', 'type': 'Métallisé'},
    'Blanc Glacier': {'name': 'Blanc Glacier', 'hex': '#FFFFFF', 'type': 'Opaque'},
    'Bleu Marine': {'name': 'Bleu Marine', 'hex': '#1B2F4B', 'type': 'Opaque'},
    'Gris Platine': {'name': 'Gris Platine', 'hex': '#C0C0C0', 'type': 'Métallisé'}
}

# APIs Principales
APIS = {
    'NHTSA': {
        'base_url': 'https://vpic.nhtsa.dot.gov/api/vehicles',
        'requires_key': False
    }
}

# Sources d'images
IMAGE_SOURCES = {
    'BRANDS': {
        'base_url': 'https://www.carlogos.org/car-logos/',
        'format': '{brand}-logo.png'
    }
}

# Exporter toutes les données
__all__ = [
    'FRENCH_BRANDS_DATA',
    'GLOBAL_BRANDS_DATA',
    'BODY_TYPES',
    'ENGINE_TYPES',
    'TRIM_LEVELS',
    'AVAILABLE_OPTIONS',
    'AVAILABLE_COLORS',
    'APIS',
    'IMAGE_SOURCES'
]
