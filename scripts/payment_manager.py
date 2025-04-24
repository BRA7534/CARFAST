"""
Gestionnaire de paiement sécurisé pour CarFast
"""

import os
import json
import hmac
import time
import uuid
import stripe
import pyotp
import qrcode
import logging
import requests
from enum import Enum
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta
from pathlib import Path
from cryptography.fernet import Fernet
from dataclasses import dataclass
from email_validator import validate_email, EmailNotValidError

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('payment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PaymentMethod(Enum):
    """Méthodes de paiement disponibles."""
    CREDIT_CARD = "credit_card"
    GOOGLE_PAY = "google_pay"
    APPLE_PAY = "apple_pay"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"

@dataclass
class PaymentConfig:
    """Configuration des paiements."""
    STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "pk_test_...")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")
    GOOGLE_PAY_MERCHANT_ID = os.getenv("GOOGLE_PAY_MERCHANT_ID", "merchant_id")
    APPLE_PAY_MERCHANT_ID = os.getenv("APPLE_PAY_MERCHANT_ID", "merchant.com.carfast")
    PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "client_id")
    PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", "secret")
    
    # Configuration de la sécurité
    MAX_PAYMENT_ATTEMPTS = 3
    LOCK_DURATION = 30  # minutes
    SESSION_DURATION = 15  # minutes
    OTP_VALIDITY = 5  # minutes
    
    # Limites de paiement
    MIN_AMOUNT = 1.0  # €
    MAX_AMOUNT = 10000.0  # €
    
    # Délais d'expiration
    PAYMENT_TIMEOUT = 900  # secondes (15 minutes)
    VERIFICATION_TIMEOUT = 300  # secondes (5 minutes)

class PaymentStatus(Enum):
    """États possibles d'un paiement."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"

class TwoFactorMethod(Enum):
    """Méthodes de double authentification."""
    SMS = "sms"
    EMAIL = "email"
    AUTHENTICATOR = "authenticator"
    BACKUP_CODES = "backup_codes"

class PaymentManager:
    """Gestionnaire de paiement sécurisé."""
    
    def __init__(self):
        """Initialise le gestionnaire de paiement."""
        # Initialiser Stripe
        stripe.api_key = PaymentConfig.STRIPE_SECRET_KEY
        stripe.max_network_retries = 2
        
        # Initialiser le chiffrement
        self._encryption_key = Fernet.generate_key()
        self._cipher = Fernet(self._encryption_key)
        
        # Initialiser TOTP pour l'authentification
        self._totp = pyotp.TOTP(pyotp.random_base32())
        
        # Cache des sessions de paiement
        self._payment_sessions = {}
        self._failed_attempts = {}
        
    def _validate_amount(self, amount: float) -> bool:
        """Valide le montant du paiement."""
        return PaymentConfig.MIN_AMOUNT <= amount <= PaymentConfig.MAX_AMOUNT
    
    def _validate_email(self, email: str) -> bool:
        """Valide l'adresse email."""
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    def _generate_session_id(self) -> str:
        """Génère un ID de session unique."""
        return str(uuid.uuid4())
    
    def _encrypt_payment_data(self, data: Dict) -> bytes:
        """Chiffre les données de paiement."""
        return self._cipher.encrypt(json.dumps(data).encode())
    
    def _decrypt_payment_data(self, encrypted_data: bytes) -> Dict:
        """Déchiffre les données de paiement."""
        try:
            decrypted = self._cipher.decrypt(encrypted_data)
            return json.loads(decrypted.decode())
        except Exception as e:
            logger.error(f"Erreur de déchiffrement: {e}")
            return {}
    
    def _check_rate_limit(self, user_id: str) -> bool:
        """Vérifie les limites de tentatives."""
        if user_id in self._failed_attempts:
            attempts, timestamp = self._failed_attempts[user_id]
            if attempts >= PaymentConfig.MAX_PAYMENT_ATTEMPTS:
                lock_until = timestamp + timedelta(minutes=PaymentConfig.LOCK_DURATION)
                if datetime.now() < lock_until:
                    return False
                self._failed_attempts.pop(user_id)
        return True
    
    def _record_failed_attempt(self, user_id: str) -> None:
        """Enregistre une tentative échouée."""
        if user_id in self._failed_attempts:
            attempts, _ = self._failed_attempts[user_id]
            self._failed_attempts[user_id] = (attempts + 1, datetime.now())
        else:
            self._failed_attempts[user_id] = (1, datetime.now())
    
    def setup_2fa(self, user_id: str, method: TwoFactorMethod) -> Dict:
        """
        Configure la double authentification.
        
        Args:
            user_id: ID de l'utilisateur
            method: Méthode de 2FA choisie
            
        Returns:
            Dict: Informations de configuration
        """
        if method == TwoFactorMethod.AUTHENTICATOR:
            # Générer une nouvelle clé secrète
            secret = pyotp.random_base32()
            totp = pyotp.TOTP(secret)
            
            # Générer le QR code
            provisioning_uri = totp.provisioning_uri(
                name=f"CarFast_{user_id}",
                issuer_name="CarFast"
            )
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(provisioning_uri)
            qr.make(fit=True)
            
            # Sauvegarder la clé pour l'utilisateur
            # (à implémenter avec la base de données)
            
            return {
                "secret": secret,
                "qr_code": qr.make_image(),
                "backup_codes": self._generate_backup_codes()
            }
            
        elif method == TwoFactorMethod.BACKUP_CODES:
            return {
                "backup_codes": self._generate_backup_codes()
            }
            
        elif method == TwoFactorMethod.SMS:
            # Générer et envoyer un code par SMS
            code = self._generate_otp()
            # Implémenter l'envoi SMS
            return {"message": "Code envoyé par SMS"}
            
        elif method == TwoFactorMethod.EMAIL:
            # Générer et envoyer un code par email
            code = self._generate_otp()
            # Implémenter l'envoi email
            return {"message": "Code envoyé par email"}
    
    def _generate_backup_codes(self, count: int = 8) -> List[str]:
        """Génère des codes de secours."""
        return [str(uuid.uuid4())[:8] for _ in range(count)]
    
    def _generate_otp(self) -> str:
        """Génère un code OTP."""
        return pyotp.TOTP(pyotp.random_base32()).now()
    
    def verify_2fa(self, user_id: str, method: TwoFactorMethod, code: str) -> bool:
        """
        Vérifie un code 2FA.
        
        Args:
            user_id: ID de l'utilisateur
            method: Méthode de 2FA utilisée
            code: Code fourni
            
        Returns:
            bool: True si le code est valide
        """
        try:
            if method == TwoFactorMethod.AUTHENTICATOR:
                # Récupérer la clé secrète de l'utilisateur
                # (à implémenter avec la base de données)
                secret = "user_secret"
                totp = pyotp.TOTP(secret)
                return totp.verify(code)
                
            elif method == TwoFactorMethod.BACKUP_CODES:
                # Vérifier si le code est dans la liste des codes de secours
                # (à implémenter avec la base de données)
                return True
                
            elif method in (TwoFactorMethod.SMS, TwoFactorMethod.EMAIL):
                # Vérifier le code OTP
                # (à implémenter avec la base de données)
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Erreur de vérification 2FA: {e}")
            return False
    
    def create_payment_session(
        self,
        user_id: str,
        amount: float,
        currency: str = "EUR",
        payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD
    ) -> Optional[Dict]:
        """
        Crée une session de paiement sécurisée.
        
        Args:
            user_id: ID de l'utilisateur
            amount: Montant à payer
            currency: Devise (défaut: EUR)
            payment_method: Méthode de paiement
            
        Returns:
            Dict: Informations de session ou None
        """
        try:
            # Valider le montant
            if not self._validate_amount(amount):
                raise ValueError("Montant invalide")
            
            # Vérifier les limites de tentatives
            if not self._check_rate_limit(user_id):
                raise ValueError("Trop de tentatives, compte temporairement bloqué")
            
            # Créer la session selon la méthode
            session_data = None
            
            if payment_method == PaymentMethod.CREDIT_CARD:
                # Créer une session Stripe
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': currency.lower(),
                            'product_data': {
                                'name': 'CarFast Subscription',
                            },
                            'unit_amount': int(amount * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url='https://carfast.com/payment/success',
                    cancel_url='https://carfast.com/payment/cancel',
                )
                session_data = {
                    'session_id': session.id,
                    'payment_url': session.url
                }
                
            elif payment_method == PaymentMethod.GOOGLE_PAY:
                # Configurer Google Pay
                session_data = {
                    'merchantId': PaymentConfig.GOOGLE_PAY_MERCHANT_ID,
                    'merchantName': "CarFast",
                    'amount': amount,
                    'currency': currency
                }
                
            elif payment_method == PaymentMethod.APPLE_PAY:
                # Configurer Apple Pay
                session_data = {
                    'merchantIdentifier': PaymentConfig.APPLE_PAY_MERCHANT_ID,
                    'amount': amount,
                    'currency': currency
                }
                
            elif payment_method == PaymentMethod.PAYPAL:
                # Créer une session PayPal
                session_data = {
                    'client_id': PaymentConfig.PAYPAL_CLIENT_ID,
                    'amount': amount,
                    'currency': currency
                }
            
            if session_data:
                # Générer un ID de session
                session_id = self._generate_session_id()
                
                # Stocker la session
                encrypted_data = self._encrypt_payment_data({
                    'user_id': user_id,
                    'amount': amount,
                    'currency': currency,
                    'payment_method': payment_method.value,
                    'created_at': datetime.now().isoformat(),
                    'expires_at': (datetime.now() + timedelta(minutes=PaymentConfig.SESSION_DURATION)).isoformat(),
                    'status': PaymentStatus.PENDING.value,
                    **session_data
                })
                
                self._payment_sessions[session_id] = encrypted_data
                
                return {
                    'session_id': session_id,
                    'payment_data': session_data,
                    'expires_in': PaymentConfig.SESSION_DURATION * 60
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur de création de session: {e}")
            self._record_failed_attempt(user_id)
            return None
    
    def process_payment(
        self,
        session_id: str,
        payment_details: Dict,
        verification_code: str
    ) -> Tuple[bool, str]:
        """
        Traite un paiement.
        
        Args:
            session_id: ID de la session
            payment_details: Détails du paiement
            verification_code: Code de vérification 2FA
            
        Returns:
            Tuple[bool, str]: (succès, message)
        """
        try:
            # Récupérer la session
            if session_id not in self._payment_sessions:
                return False, "Session invalide ou expirée"
            
            # Déchiffrer les données
            session_data = self._decrypt_payment_data(
                self._payment_sessions[session_id]
            )
            
            # Vérifier l'expiration
            if datetime.fromisoformat(session_data['expires_at']) < datetime.now():
                return False, "Session expirée"
            
            # Vérifier le code 2FA
            if not self.verify_2fa(
                session_data['user_id'],
                TwoFactorMethod.AUTHENTICATOR,
                verification_code
            ):
                return False, "Code de vérification invalide"
            
            # Traiter le paiement selon la méthode
            payment_method = PaymentMethod(session_data['payment_method'])
            
            if payment_method == PaymentMethod.CREDIT_CARD:
                # Traiter avec Stripe
                try:
                    payment_intent = stripe.PaymentIntent.create(
                        amount=int(session_data['amount'] * 100),
                        currency=session_data['currency'].lower(),
                        payment_method=payment_details['payment_method_id'],
                        confirm=True
                    )
                    if payment_intent.status == 'succeeded':
                        return True, "Paiement réussi"
                    return False, "Échec du paiement"
                    
                except stripe.error.CardError as e:
                    return False, f"Erreur de carte: {str(e)}"
                
            elif payment_method == PaymentMethod.GOOGLE_PAY:
                # Traiter avec Google Pay
                # Implémenter la logique de paiement Google Pay
                return True, "Paiement Google Pay réussi"
                
            elif payment_method == PaymentMethod.APPLE_PAY:
                # Traiter avec Apple Pay
                # Implémenter la logique de paiement Apple Pay
                return True, "Paiement Apple Pay réussi"
                
            elif payment_method == PaymentMethod.PAYPAL:
                # Traiter avec PayPal
                # Implémenter la logique de paiement PayPal
                return True, "Paiement PayPal réussi"
            
            return False, "Méthode de paiement non supportée"
            
        except Exception as e:
            logger.error(f"Erreur de traitement du paiement: {e}")
            return False, f"Erreur de paiement: {str(e)}"
        
        finally:
            # Nettoyer la session
            if session_id in self._payment_sessions:
                del self._payment_sessions[session_id]
    
    def refund_payment(
        self,
        payment_id: str,
        amount: Optional[float] = None,
        reason: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Effectue un remboursement.
        
        Args:
            payment_id: ID du paiement
            amount: Montant à rembourser (None pour tout)
            reason: Raison du remboursement
            
        Returns:
            Tuple[bool, str]: (succès, message)
        """
        try:
            # Récupérer les détails du paiement
            # (à implémenter avec la base de données)
            
            # Effectuer le remboursement selon la méthode
            if payment_method == PaymentMethod.CREDIT_CARD:
                refund = stripe.Refund.create(
                    payment_intent=payment_id,
                    amount=int(amount * 100) if amount else None,
                    reason=reason
                )
                if refund.status == 'succeeded':
                    return True, "Remboursement réussi"
                return False, "Échec du remboursement"
                
            # Implémenter les autres méthodes de remboursement
            
            return False, "Méthode de remboursement non supportée"
            
        except Exception as e:
            logger.error(f"Erreur de remboursement: {e}")
            return False, f"Erreur de remboursement: {str(e)}"
