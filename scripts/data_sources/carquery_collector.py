import requests
import time
from typing import List, Dict, Any
from .config import APIS

class CarQueryCollector:
    def __init__(self):
        self.base_url = APIS['CARQUERY']['base_url']
        self.session = requests.Session()
        self.rate_limit_delay = 1

    def get_all_makes(self, year: int = None) -> List[Dict[str, Any]]:
        """Récupère toutes les marques disponibles."""
        params = {'cmd': 'getMakes'}
        if year:
            params['year'] = year
        
        return self._make_request(params)

    def get_models(self, make: str, year: int = None) -> List[Dict[str, Any]]:
        """Récupère tous les modèles pour une marque donnée."""
        params = {
            'cmd': 'getModels',
            'make': make
        }
        if year:
            params['year'] = year
        
        return self._make_request(params)

    def get_model_details(self, model_id: str) -> Dict[str, Any]:
        """Récupère les détails d'un modèle spécifique."""
        params = {
            'cmd': 'getModel',
            'model': model_id
        }
        
        return self._make_request(params)

    def get_model_trims(self, make: str, model: str, year: int) -> List[Dict[str, Any]]:
        """Récupère les différentes versions d'un modèle."""
        params = {
            'cmd': 'getTrims',
            'make': make,
            'model': model,
            'year': year
        }
        
        return self._make_request(params)

    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Effectue une requête HTTP avec gestion des erreurs et rate limiting."""
        try:
            time.sleep(self.rate_limit_delay)
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête CarQuery: {str(e)}")
            return {}
        except ValueError as e:
            print(f"Erreur lors du parsing de la réponse CarQuery: {str(e)}")
            return {}

    def collect_full_data(self, start_year: int, end_year: int) -> Dict[str, Any]:
        """Collecte toutes les données disponibles pour une période donnée."""
        full_data = {
            'makes': {},
            'models': {},
            'trims': {}
        }

        for year in range(start_year, end_year + 1):
            print(f"Collecte des données CarQuery pour {year}...")
            
            # Récupérer toutes les marques
            makes = self.get_all_makes(year)
            for make in makes:
                make_name = make.get('make_display')
                if not make_name:
                    continue

                # Stocker les informations de la marque
                if make_name not in full_data['makes']:
                    full_data['makes'][make_name] = make

                # Récupérer les modèles
                models = self.get_models(make_name, year)
                if make_name not in full_data['models']:
                    full_data['models'][make_name] = {}
                
                for model in models:
                    model_name = model.get('model_name')
                    if not model_name:
                        continue

                    # Récupérer les détails du modèle
                    model_details = self.get_model_details(model.get('model_id'))
                    
                    if year not in full_data['models'][make_name]:
                        full_data['models'][make_name][year] = {}
                    
                    full_data['models'][make_name][year][model_name] = model_details

                    # Récupérer les versions
                    trims = self.get_model_trims(make_name, model_name, year)
                    if make_name not in full_data['trims']:
                        full_data['trims'][make_name] = {}
                    if year not in full_data['trims'][make_name]:
                        full_data['trims'][make_name][year] = {}
                    full_data['trims'][make_name][year][model_name] = trims

        return full_data
