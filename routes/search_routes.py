"""
Routes pour la recherche de véhicules avec performances optimisées
"""

from flask import Blueprint, jsonify, request, current_app
from flask_caching import Cache
from scripts.data_sources.reviews_collector import ReviewsCollector
from scripts.subscription_manager import SubscriptionManager
from scripts.payment_manager import PaymentManager
from scripts.search_optimizer import SearchOptimizer
from marshmallow import Schema, fields, validate
from functools import wraps
import jwt
import logging

search_bp = Blueprint('search', __name__)
reviews_collector = ReviewsCollector()
subscription_manager = SubscriptionManager()
payment_manager = PaymentManager()
search_optimizer = SearchOptimizer()
cache = Cache()

class SearchParamsSchema(Schema):
    make = fields.Str(allow_none=True)
    model = fields.Str(allow_none=True)
    year_min = fields.Int(allow_none=True, validate=validate.Range(min=1900))
    year_max = fields.Int(allow_none=True, validate=validate.Range(max=2025))
    price_min = fields.Float(allow_none=True, validate=validate.Range(min=0))
    price_max = fields.Float(allow_none=True)
    mileage_min = fields.Int(allow_none=True, validate=validate.Range(min=0))
    mileage_max = fields.Int(allow_none=True)
    fuel_type = fields.Str(allow_none=True, validate=validate.OneOf(['essence', 'diesel', 'électrique', 'hybride']))
    transmission = fields.Str(allow_none=True, validate=validate.OneOf(['manuelle', 'automatique']))
    location = fields.Str(allow_none=True)
    radius = fields.Int(allow_none=True, validate=validate.Range(min=0, max=1000))
    sort_by = fields.Str(missing='relevance', validate=validate.OneOf(['relevance', 'price_asc', 'price_desc', 'year_desc', 'mileage_asc']))
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    limit = fields.Int(missing=20, validate=validate.Range(min=1, max=100))

def require_subscription(f):
    """Décorateur pour vérifier l'abonnement avec cache."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Non autorisé'}), 401
            
        try:
            # Vérifier l'abonnement (avec cache)
            user_id = request.user['id']
            cache_key = f'subscription_{user_id}'
            subscription = cache.get(cache_key)
            
            if subscription is None:
                subscription = subscription_manager.get_subscription_info(user_id)
                if subscription:
                    cache.set(cache_key, subscription, timeout=300)  # Cache 5 minutes
            
            if not subscription or not subscription['is_active']:
                return jsonify({
                    'error': 'Abonnement requis',
                    'subscription_required': True
                }), 403
                
            return f(*args, **kwargs)
            
        except Exception as e:
            logging.error(f"Erreur de vérification d'abonnement: {str(e)}")
            return jsonify({'error': str(e)}), 500
            
    return decorated

@search_bp.route('/api/search/vehicles', methods=['GET'])
@require_subscription
def search_vehicles():
    """Recherche de véhicules avec cache et optimisation."""
    try:
        # Valider et nettoyer les paramètres
        schema = SearchParamsSchema()
        params = schema.load(request.args)
        
        # Générer une clé de cache unique
        cache_key = f"search_{hash(frozenset(params.items()))}"
        results = cache.get(cache_key)
        
        if results is None:
            # Optimiser la recherche
            optimized_params = search_optimizer.optimize_query(params)
            
            # Effectuer la recherche
            results = reviews_collector.search_vehicles(optimized_params)
            
            # Mettre en cache les résultats
            cache.set(cache_key, results, timeout=60)  # Cache 1 minute
            
        return jsonify({
            'success': True,
            'results': results['vehicles'],
            'total': results['total'],
            'page': params['page'],
            'pages': results['pages'],
            'filters': search_optimizer.get_available_filters(results),
            'suggestions': search_optimizer.get_search_suggestions(params)
        })
        
    except Exception as e:
        logging.error(f"Erreur de recherche: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/api/search/reviews', methods=['GET'])
@require_subscription
def search_reviews():
    """Recherche d'avis."""
    try:
        # Paramètres de recherche
        params = {
            'vehicle_id': request.args.get('vehicle_id'),
            'rating_min': request.args.get('rating_min'),
            'rating_max': request.args.get('rating_max'),
            'sort_by': request.args.get('sort_by', 'date'),
            'page': int(request.args.get('page', 1)),
            'limit': int(request.args.get('limit', 20))
        }
        
        # Vérifier les jetons disponibles
        subscription = subscription_manager.get_subscription_info(request.user['id'])
        if subscription['remaining_tokens'] < 1:
            return jsonify({
                'error': 'Jetons insuffisants',
                'tokens_required': True
            }), 403
            
        # Effectuer la recherche
        results = reviews_collector.search_reviews(params)
        
        # Déduire un jeton
        subscription_manager.use_tokens(request.user['id'], 1)
        
        return jsonify({
            'success': True,
            'results': results['reviews'],
            'total': results['total'],
            'page': params['page'],
            'pages': results['pages']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/api/search/suggestions', methods=['GET'])
def get_suggestions():
    """Suggestions de recherche."""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify([])
            
        # Obtenir les suggestions
        suggestions = reviews_collector.get_suggestions(query)
        
        return jsonify(suggestions)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@search_bp.route('/api/search/filters', methods=['GET'])
def get_filters():
    """Récupère les filtres disponibles."""
    try:
        filters = {
            'makes': reviews_collector.get_makes(),
            'models': reviews_collector.get_models(request.args.get('make')),
            'years': reviews_collector.get_years(),
            'fuel_types': [
                'Essence', 'Diesel', 'Électrique', 'Hybride',
                'Hybride rechargeable', 'GPL', 'Hydrogène'
            ],
            'transmissions': ['Manuelle', 'Automatique'],
            'sort_options': [
                {'value': 'relevance', 'label': 'Pertinence'},
                {'value': 'price_asc', 'label': 'Prix croissant'},
                {'value': 'price_desc', 'label': 'Prix décroissant'},
                {'value': 'year_desc', 'label': 'Plus récent'},
                {'value': 'year_asc', 'label': 'Plus ancien'},
                {'value': 'mileage_asc', 'label': 'Kilométrage croissant'},
                {'value': 'mileage_desc', 'label': 'Kilométrage décroissant'}
            ]
        }
        
        return jsonify(filters)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@search_bp.route('/api/search/save', methods=['POST'])
@require_subscription
def save_search():
    """Sauvegarde une recherche."""
    try:
        data = request.json
        
        # Vérifier le nombre de recherches sauvegardées
        subscription = subscription_manager.get_subscription_info(request.user['id'])
        current_searches = subscription.get('saved_searches', [])
        
        if len(current_searches) >= subscription['max_saved_searches']:
            return jsonify({
                'error': 'Limite de recherches sauvegardées atteinte',
                'upgrade_required': True
            }), 403
            
        # Sauvegarder la recherche
        search_id = reviews_collector.save_search(
            user_id=request.user['id'],
            params=data['params'],
            name=data.get('name', 'Recherche sauvegardée')
        )
        
        return jsonify({
            'success': True,
            'search_id': search_id
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/api/search/saved', methods=['GET'])
@require_subscription
def get_saved_searches():
    """Récupère les recherches sauvegardées."""
    try:
        searches = reviews_collector.get_saved_searches(request.user['id'])
        
        return jsonify({
            'success': True,
            'searches': searches
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/api/search/delete/<search_id>', methods=['DELETE'])
@require_subscription
def delete_saved_search(search_id):
    """Supprime une recherche sauvegardée."""
    try:
        success = reviews_collector.delete_saved_search(
            user_id=request.user['id'],
            search_id=search_id
        )
        
        return jsonify({
            'success': success
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
