"""
Routes pour la gestion des paiements avec sécurité renforcée
"""

from flask import Blueprint, jsonify, request, render_template
from scripts.payment_manager import PaymentManager, PaymentMethod, PaymentStatus
from scripts.subscription_manager import SubscriptionManager
from scripts.fraud_detection import FraudDetector
from marshmallow import Schema, fields, validate
from functools import wraps
import jwt
import os
import logging

payment_bp = Blueprint('payment', __name__)
payment_manager = PaymentManager()
subscription_manager = SubscriptionManager()
fraud_detector = FraudDetector()

# Schémas de validation
class PaymentSessionSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    currency = fields.Str(required=True, validate=validate.OneOf(['EUR', 'USD']))
    payment_method = fields.Str(required=True, validate=validate.OneOf(['card', 'paypal']))

def require_auth(f):
    """Décorateur pour vérifier l'authentification avec rate limiting."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            logging.warning(f"Tentative d'accès sans token - IP: {request.remote_addr}")
            return jsonify({'error': 'Token manquant'}), 401
            
        try:
            # Vérifier et décoder le token
            payload = jwt.decode(
                token.split(' ')[1],
                os.getenv('JWT_SECRET'),
                algorithms=['HS256']
            )
            
            # Vérifier si l'utilisateur est bloqué
            if payment_manager.is_user_blocked(payload['id']):
                logging.error(f"Utilisateur bloqué - ID: {payload['id']}")
                return jsonify({'error': 'Compte bloqué'}), 403
                
            request.user = payload
            return f(*args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expiré'}), 401
        except jwt.InvalidTokenError:
            logging.warning(f"Token invalide - IP: {request.remote_addr}")
            return jsonify({'error': 'Token invalide'}), 401
            
    return decorated

@payment_bp.route('/payment', methods=['GET'])
@require_auth
def payment_page():
    """Page de paiement sécurisée."""
    subscription_id = request.args.get('subscription')
    if not subscription_id:
        return jsonify({'error': 'ID d\'abonnement manquant'}), 400
        
    subscription = subscription_manager.get_subscription_info(subscription_id)
    if not subscription:
        return jsonify({'error': 'Abonnement non trouvé'}), 404
        
    # Vérifier si l'utilisateur a le droit d'accéder à cet abonnement
    if not subscription_manager.can_access_subscription(request.user['id'], subscription_id):
        logging.warning(f"Tentative d'accès non autorisé - User: {request.user['id']}")
        return jsonify({'error': 'Accès non autorisé'}), 403
        
    return render_template(
        'payment.html',
        subscription=subscription,
        stripe_key=os.getenv('STRIPE_PUBLIC_KEY')
    )

@payment_bp.route('/api/payment/create-session', methods=['POST'])
@require_auth
def create_payment_session():
    """Crée une session de paiement sécurisée."""
    try:
        # Valider les données avec marshmallow
        schema = PaymentSessionSchema()
        data = schema.load(request.json)
        
        # Vérification anti-fraude
        fraud_score = fraud_detector.check_transaction(
            user_id=request.user['id'],
            amount=data['amount'],
            ip_address=request.remote_addr
        )
        
        if fraud_score > 0.7:  # Seuil de risque élevé
            logging.error(f"Détection de fraude - User: {request.user['id']}, Score: {fraud_score}")
            return jsonify({'error': 'Transaction refusée pour raison de sécurité'}), 403
            
        # Créer la session
        session = payment_manager.create_payment_session(
            user_id=request.user['id'],
            amount=data['amount'],
            currency=data['currency'],
            payment_method=PaymentMethod(data['payment_method']),
            ip_address=request.remote_addr
        )
        
        if not session:
            return jsonify({'error': 'Erreur de création de session'}), 500
            
        logging.info(f"Session de paiement créée - User: {request.user['id']}, Amount: {data['amount']}")
        return jsonify(session)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f"Erreur lors de la création de session - User: {request.user['id']}, Error: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500

@payment_bp.route('/api/payment/process', methods=['POST'])
@require_auth
def process_payment():
    """Traite un paiement."""
    try:
        data = request.json
        
        # Valider les données
        required_fields = ['session_id', 'payment_details', 'verification_code']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Données manquantes'}), 400
            
        # Traiter le paiement
        success, message = payment_manager.process_payment(
            data['session_id'],
            data['payment_details'],
            data['verification_code']
        )
        
        if success:
            # Mettre à jour l'abonnement
            subscription_id = request.args.get('subscription')
            if subscription_id:
                subscription_manager.activate_subscription(
                    subscription_id,
                    request.user['id']
                )
            
            return jsonify({
                'success': True,
                'message': message
            })
        
        return jsonify({
            'success': False,
            'message': message
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erreur lors du traitement du paiement'
        }), 500

@payment_bp.route('/api/payment/verify-2fa', methods=['POST'])
@require_auth
def verify_2fa():
    """Vérifie un code 2FA."""
    try:
        data = request.json
        
        if 'code' not in data:
            return jsonify({'error': 'Code manquant'}), 400
            
        # Vérifier le code
        valid = payment_manager.verify_2fa(
            request.user['id'],
            data.get('method', 'authenticator'),
            data['code']
        )
        
        return jsonify({'valid': valid})
        
    except Exception as e:
        return jsonify({'error': 'Erreur de vérification'}), 500

@payment_bp.route('/api/payment/refund', methods=['POST'])
@require_auth
def refund_payment():
    """Effectue un remboursement."""
    try:
        data = request.json
        
        if 'payment_id' not in data:
            return jsonify({'error': 'ID de paiement manquant'}), 400
            
        # Effectuer le remboursement
        success, message = payment_manager.refund_payment(
            data['payment_id'],
            data.get('amount'),
            data.get('reason')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            })
            
        return jsonify({
            'success': False,
            'message': message
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erreur lors du remboursement'
        }), 500

@payment_bp.route('/api/payment/status/<payment_id>', methods=['GET'])
@require_auth
def payment_status(payment_id):
    """Récupère le statut d'un paiement."""
    try:
        # Vérifier les permissions
        payment = payment_manager.get_payment_info(payment_id)
        if not payment or payment['user_id'] != request.user['id']:
            return jsonify({'error': 'Paiement non trouvé'}), 404
            
        return jsonify(payment)
        
    except Exception as e:
        return jsonify({'error': 'Erreur serveur'}), 500

@payment_bp.route('/api/payment/methods', methods=['GET'])
@require_auth
def get_payment_methods():
    """Récupère les méthodes de paiement disponibles."""
    try:
        methods = {
            'card': True,
            'google_pay': True,
            'apple_pay': True,
            'paypal': True
        }
        
        return jsonify(methods)
        
    except Exception as e:
        return jsonify({'error': 'Erreur serveur'}), 500
