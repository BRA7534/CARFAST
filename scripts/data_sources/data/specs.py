"""Spécifications techniques communes"""

# Types de carrosserie
BODY_TYPES = {
    'Citadine': ['Renault Clio', 'Peugeot 208', 'Toyota Yaris', 'VW Polo'],
    'Berline Compacte': ['Renault Megane', 'Peugeot 308', 'VW Golf', 'BMW Série 1'],
    'Berline': ['Peugeot 508', 'VW Passat', 'BMW Série 3', 'Mercedes Classe C'],
    'Break': ['Peugeot 308 SW', 'VW Passat SW', 'BMW Série 3 Touring', 'Mercedes Classe C Break'],
    'SUV Compact': ['Renault Captur', 'Peugeot 2008', 'VW T-Roc', 'BMW X1'],
    'SUV': ['Peugeot 3008', 'VW Tiguan', 'BMW X3', 'Mercedes GLC'],
    'Monospace': ['Renault Scenic', 'BMW Série 2 Active Tourer', 'Mercedes Classe B'],
    'Coupé': ['BMW Série 4', 'Mercedes Classe C Coupé', 'Audi A5'],
    'Cabriolet': ['BMW Série 4 Cabriolet', 'Mercedes Classe C Cabriolet', 'Audi A5 Cabriolet']
}

# Types de motorisation
ENGINE_TYPES = {
    'Essence': {
        'puissances': [70, 90, 110, 130, 150, 180, 200, 250, 300, 350, 400],
        'cylindrees': [999, 1199, 1332, 1498, 1984, 2979, 2998]
    },
    'Diesel': {
        'puissances': [90, 110, 130, 150, 180, 200, 250, 300, 350],
        'cylindrees': [1461, 1498, 1995, 2993]
    },
    'Hybride': {
        'puissances': [140, 160, 180, 200, 225, 250, 300],
        'types': ['HEV', 'MHEV']
    },
    'Hybride Rechargeable': {
        'puissances': [180, 225, 250, 300, 360, 400],
        'types': ['PHEV']
    },
    'Électrique': {
        'puissances': [136, 150, 170, 204, 245, 300, 408, 450, 500],
        'batteries': [40, 50, 60, 77, 82, 100, 120]
    }
}

# Niveaux de finition par segment
TRIM_LEVELS = {
    'Entrée de gamme': ['Life', 'Active', 'Trendline', 'SE'],
    'Milieu de gamme': ['Zen', 'Allure', 'Style', 'Comfort'],
    'Haut de gamme': ['Intens', 'GT Line', 'R-Line', 'M Sport'],
    'Premium': ['Initiale Paris', 'GT', 'R', 'M'],
    'Sport': ['RS', 'GTI', 'M', 'AMG']
}

# Options disponibles par catégorie
AVAILABLE_OPTIONS = {
    'Sécurité': [
        'Freinage d\'urgence automatique',
        'Régulateur adaptatif',
        'Surveillance d\'angle mort',
        'Alerte de franchissement de ligne',
        'Vision nocturne',
        'Caméra 360°'
    ],
    'Confort': [
        'Climatisation automatique bi-zone',
        'Sièges chauffants',
        'Sièges ventilés',
        'Sièges massants',
        'Toit ouvrant panoramique',
        'Hayon électrique',
        'Accès et démarrage mains libres'
    ],
    'Multimédia': [
        'Navigation connectée',
        'Apple CarPlay / Android Auto',
        'Système audio premium',
        'Affichage tête haute',
        'Écran tactile 10"',
        'Instrumentation numérique',
        'Chargeur smartphone à induction'
    ],
    'Design': [
        'Jantes alliage',
        'Vitres surteintées',
        'Peinture métallisée',
        'Pack Sport',
        'Sellerie cuir',
        'Éclairage d\'ambiance',
        'Toit contrasté'
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
    'Gris Platine': {'name': 'Gris Platine', 'hex': '#C0C0C0', 'type': 'Métallisé'},
    'Beige Dune': {'name': 'Beige Dune', 'hex': '#CFC1A8', 'type': 'Métallisé'},
    'Brun Vison': {'name': 'Brun Vison', 'hex': '#5C4033', 'type': 'Métallisé'}
}
