"""
Module d'importation des données
"""

from .french_brands import FRENCH_BRANDS
from .german_brands import GERMAN_BRANDS
from .asian_brands import ASIAN_BRANDS
from .american_brands import AMERICAN_BRANDS
from .specs import (
    BODY_TYPES,
    ENGINE_TYPES,
    TRIM_LEVELS,
    AVAILABLE_OPTIONS,
    AVAILABLE_COLORS
)

# Fusionner toutes les marques
ALL_BRANDS = {
    **FRENCH_BRANDS,
    **GERMAN_BRANDS,
    **ASIAN_BRANDS,
    **AMERICAN_BRANDS
}
