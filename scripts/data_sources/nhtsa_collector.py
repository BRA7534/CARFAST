import requests
import time
from typing import List, Dict, Any
from .config import APIS, MAIN_BRANDS

class NHTSACollector:
    def __init__(self):
        self.base_url = APIS['NHTSA']['base_url']
        self.session = requests.Session()
        self.rate_limit_delay = 1  # Délai entre les requêtes en secondes

    def get_all_makes(self, year: int = None) -> List[Dict[str, Any]]:
        """Récupère toutes les marques de véhicules."""
        endpoint = f"{self.base_url}/GetAllMakes?format=json"
        if year:
            endpoint += f"&year={year}"
        
        response = self._make_request(endpoint)
        return response.get('Results', [])

    def get_models_for_make(self, make: str, year: int = None) -> List[Dict[str, Any]]:
        """Récupère tous les modèles pour une marque et une année données."""
        # Encoder le nom de la marque pour l'URL
        encoded_make = requests.utils.quote(make)
        endpoint = f"{self.base_url}/GetModelsForMake/{encoded_make}?format=json"
        if year:
            endpoint += f"&year={year}"
        
        response = self._make_request(endpoint)
        return response.get('Results', [])

    def get_vehicle_types_for_make(self, make: str) -> List[Dict[str, Any]]:
        """Récupère tous les types de véhicules pour une marque donnée."""
        # Encoder le nom de la marque pour l'URL
        encoded_make = requests.utils.quote(make)
        endpoint = f"{self.base_url}/GetVehicleTypesForMake/{encoded_make}?format=json"
        
        response = self._make_request(endpoint)
        return response.get('Results', [])

    def get_make_details(self, make: str) -> Dict[str, Any]:
        """Récupère les détails d'une marque spécifique."""
        # Encoder le nom de la marque pour l'URL
        encoded_make = requests.utils.quote(make)
        endpoint = f"{self.base_url}/GetMakeForManufacturer/{encoded_make}?format=json"
        
        response = self._make_request(endpoint)
        results = response.get('Results', [])
        return results[0] if results else {}

    def get_model_details(self, make: str, model: str, year: int) -> Dict[str, Any]:
        """Récupère les détails d'un modèle spécifique."""
        endpoint = f"{self.base_url}/DecodeModelYear/make/{make}/model/{model}/year/{year}?format=json"
        
        response = self._make_request(endpoint)
        results = response.get('Results', [])
        return results[0] if results else {}

    def _make_request(self, url: str) -> Dict[str, Any]:
        """Effectue une requête HTTP avec gestion des erreurs et rate limiting."""
        try:
            time.sleep(self.rate_limit_delay)  # Respecter le rate limiting
            
            # Encoder correctement l'URL
            encoded_url = requests.utils.quote(url, safe=':/?=&')
            response = self.session.get(encoded_url)
            
            if response.status_code == 404:
                print(f"Resource not found: {url}")
                return {'Results': []}
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête à {url}: {str(e)}")
            return {'Results': []}
        except ValueError as e:
            print(f"Erreur lors du parsing de la réponse de {url}: {str(e)}")
            return {'Results': []}

    def collect_full_data(self, start_year: int, end_year: int) -> Dict[str, Any]:
        """Collecte toutes les données disponibles pour une période donnée."""
        full_data = {
            'makes': {},
            'models': {},
            'types': {}
        }

        # Collecter les données pour chaque année
        for year in range(start_year, end_year + 1):
            print(f"Collecte des données pour l'année {year}...")
            
            # Récupérer les marques principales uniquement
            for make in MAIN_BRANDS:
                try:
                    print(f"  Traitement de {make}...")
                    
                    # Récupérer les informations de la marque
                    make_details = self.get_make_details(make)
                    if make_details:
                        full_data['makes'][make] = make_details

                    # Récupérer les modèles pour cette marque
                    models = self.get_models_for_make(make, year)
                    if make not in full_data['models']:
                        full_data['models'][make] = {}
                    
                    if models:
                        for model in models:
                            model_name = model.get('Model_Name')
                            if not model_name:
                                continue

                            # Récupérer les détails du modèle
                            model_details = self.get_model_details(make, model_name, year)
                            if year not in full_data['models'][make]:
                                full_data['models'][make][year] = {}
                            full_data['models'][make][year][model_name] = model_details

                        # Récupérer les types de véhicules
                        if make not in full_data['types']:
                            types = self.get_vehicle_types_for_make(make)
                            full_data['types'][make] = types

                except Exception as e:
                    print(f"  Erreur lors du traitement de {make}: {str(e)}")
                    continue

        return full_data
