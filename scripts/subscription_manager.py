"""
Gestionnaire d'abonnements et de jetons pour CarFast
"""

import json
import sqlite3
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Optional, Tuple
from pathlib import Path

class SubscriptionTier(Enum):
    """Niveaux d'abonnement disponibles."""
    
    BASIC = "basic"          # Particuliers, usage occasionnel
    PRO = "pro"             # Professionnels indépendants
    BUSINESS = "business"    # Concessions, garages
    ENTERPRISE = "enterprise"  # Grands groupes automobiles

class SubscriptionFeatures:
    """Caractéristiques des différents abonnements."""
    
    TIERS = {
        SubscriptionTier.BASIC: {
            "price_monthly": 9.99,  # €/mois
            "price_yearly": 99.99,  # €/an (environ 2 mois gratuits)
            "tokens_monthly": 100,  # Jetons par mois
            "max_saved_searches": 5,
            "max_alerts": 3,
            "features": {
                "basic_search": True,
                "advanced_search": False,
                "export_data": False,
                "api_access": False,
                "priority_support": False,
                "custom_reports": False
            }
        },
        SubscriptionTier.PRO: {
            "price_monthly": 29.99,
            "price_yearly": 299.99,
            "tokens_monthly": 500,
            "max_saved_searches": 20,
            "max_alerts": 10,
            "features": {
                "basic_search": True,
                "advanced_search": True,
                "export_data": True,
                "api_access": False,
                "priority_support": False,
                "custom_reports": False
            }
        },
        SubscriptionTier.BUSINESS: {
            "price_monthly": 99.99,
            "price_yearly": 999.99,
            "tokens_monthly": 2000,
            "max_saved_searches": 100,
            "max_alerts": 50,
            "features": {
                "basic_search": True,
                "advanced_search": True,
                "export_data": True,
                "api_access": True,
                "priority_support": True,
                "custom_reports": False
            }
        },
        SubscriptionTier.ENTERPRISE: {
            "price_monthly": 299.99,
            "price_yearly": 2999.99,
            "tokens_monthly": 10000,
            "max_saved_searches": -1,  # Illimité
            "max_alerts": -1,  # Illimité
            "features": {
                "basic_search": True,
                "advanced_search": True,
                "export_data": True,
                "api_access": True,
                "priority_support": True,
                "custom_reports": True
            }
        }
    }
    
    # Coût en jetons par type d'opération
    OPERATION_COSTS = {
        "basic_search": 1,
        "advanced_search": 2,
        "full_review": 5,
        "market_analysis": 10,
        "price_prediction": 15,
        "custom_report": 25
    }

class SubscriptionManager:
    """Gestionnaire des abonnements et des jetons."""
    
    def __init__(self, db_path: str):
        """
        Initialise le gestionnaire d'abonnements.
        
        Args:
            db_path: Chemin vers la base de données SQLite
        """
        self.db_path = db_path
        self._init_database()
        
    def _init_database(self) -> None:
        """Initialise la base de données des abonnements."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('PRAGMA foreign_keys = ON')
            
            # Table des abonnements
            conn.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                user_id INTEGER PRIMARY KEY,
                tier TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                payment_status TEXT NOT NULL,
                last_payment_date TEXT,
                next_payment_date TEXT,
                remaining_tokens INTEGER NOT NULL DEFAULT 0,
                total_tokens_used INTEGER NOT NULL DEFAULT 0
            )
            ''')
            
            # Table de l'historique des jetons
            conn.execute('''
            CREATE TABLE IF NOT EXISTS token_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                operation_type TEXT NOT NULL,
                tokens_used INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                details TEXT,
                FOREIGN KEY (user_id) REFERENCES subscriptions(user_id)
            )
            ''')
            
            # Table des bonus et promotions
            conn.execute('''
            CREATE TABLE IF NOT EXISTS token_bonuses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                bonus_type TEXT NOT NULL,
                tokens_amount INTEGER NOT NULL,
                expiry_date TEXT,
                is_used BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES subscriptions(user_id)
            )
            ''')
            
            conn.commit()
    
    def create_subscription(
        self,
        user_id: int,
        tier: SubscriptionTier,
        payment_method: str
    ) -> bool:
        """
        Crée un nouvel abonnement.
        
        Args:
            user_id: ID de l'utilisateur
            tier: Niveau d'abonnement
            payment_method: Méthode de paiement
            
        Returns:
            bool: True si l'abonnement est créé avec succès
        """
        try:
            now = datetime.now()
            
            # Calculer les dates
            start_date = now
            end_date = now + timedelta(days=30)
            next_payment = end_date - timedelta(days=3)
            
            # Obtenir les jetons initiaux
            initial_tokens = SubscriptionFeatures.TIERS[tier]["tokens_monthly"]
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                INSERT INTO subscriptions (
                    user_id, tier, start_date, end_date, is_active,
                    payment_status, last_payment_date, next_payment_date,
                    remaining_tokens
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id, tier.value, start_date.isoformat(),
                    end_date.isoformat(), True, "active",
                    now.isoformat(), next_payment.isoformat(),
                    initial_tokens
                ))
                
                # Ajouter un bonus de bienvenue
                welcome_bonus = int(initial_tokens * 0.1)  # 10% de bonus
                conn.execute('''
                INSERT INTO token_bonuses (
                    user_id, bonus_type, tokens_amount, expiry_date
                ) VALUES (?, ?, ?, ?)
                ''', (
                    user_id, "welcome_bonus", welcome_bonus,
                    (now + timedelta(days=30)).isoformat()
                ))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de l'abonnement: {e}")
            return False
    
    def check_tokens(self, user_id: int) -> Tuple[int, int]:
        """
        Vérifie le solde de jetons d'un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Tuple[int, int]: (jetons restants, total utilisé)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                SELECT remaining_tokens, total_tokens_used
                FROM subscriptions
                WHERE user_id = ? AND is_active = 1
                ''', (user_id,))
                
                result = cursor.fetchone()
                if result:
                    return result[0], result[1]
                return 0, 0
                
        except sqlite3.Error:
            return 0, 0
    
    def use_tokens(
        self,
        user_id: int,
        operation_type: str,
        details: Optional[str] = None
    ) -> bool:
        """
        Utilise des jetons pour une opération.
        
        Args:
            user_id: ID de l'utilisateur
            operation_type: Type d'opération
            details: Détails optionnels de l'opération
            
        Returns:
            bool: True si l'opération est autorisée et les jetons sont déduits
        """
        try:
            # Vérifier le coût de l'opération
            cost = SubscriptionFeatures.OPERATION_COSTS.get(operation_type)
            if not cost:
                return False
            
            with sqlite3.connect(self.db_path) as conn:
                # Vérifier le solde
                cursor = conn.execute('''
                SELECT remaining_tokens, tier
                FROM subscriptions
                WHERE user_id = ? AND is_active = 1
                ''', (user_id,))
                
                result = cursor.fetchone()
                if not result or result[0] < cost:
                    return False
                
                remaining_tokens, tier = result
                
                # Appliquer des réductions selon le niveau d'abonnement
                if tier == SubscriptionTier.BUSINESS.value:
                    cost = int(cost * 0.8)  # 20% de réduction
                elif tier == SubscriptionTier.ENTERPRISE.value:
                    cost = int(cost * 0.6)  # 40% de réduction
                
                # Déduire les jetons
                conn.execute('''
                UPDATE subscriptions
                SET remaining_tokens = remaining_tokens - ?,
                    total_tokens_used = total_tokens_used + ?
                WHERE user_id = ?
                ''', (cost, cost, user_id))
                
                # Enregistrer l'utilisation
                conn.execute('''
                INSERT INTO token_history (
                    user_id, operation_type, tokens_used, timestamp, details
                ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    user_id, operation_type, cost,
                    datetime.now().isoformat(), details
                ))
                
                conn.commit()
                return True
                
        except sqlite3.Error:
            return False
    
    def add_bonus_tokens(
        self,
        user_id: int,
        amount: int,
        bonus_type: str,
        expiry_days: int = 30
    ) -> bool:
        """
        Ajoute des jetons bonus à un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur
            amount: Nombre de jetons à ajouter
            bonus_type: Type de bonus
            expiry_days: Nombre de jours avant expiration
            
        Returns:
            bool: True si les jetons sont ajoutés avec succès
        """
        try:
            expiry_date = datetime.now() + timedelta(days=expiry_days)
            
            with sqlite3.connect(self.db_path) as conn:
                # Ajouter le bonus
                conn.execute('''
                INSERT INTO token_bonuses (
                    user_id, bonus_type, tokens_amount, expiry_date
                ) VALUES (?, ?, ?, ?)
                ''', (
                    user_id, bonus_type, amount,
                    expiry_date.isoformat()
                ))
                
                # Mettre à jour le solde
                conn.execute('''
                UPDATE subscriptions
                SET remaining_tokens = remaining_tokens + ?
                WHERE user_id = ?
                ''', (amount, user_id))
                
                conn.commit()
                return True
                
        except sqlite3.Error:
            return False
    
    def get_subscription_info(self, user_id: int) -> Optional[Dict]:
        """
        Récupère les informations d'abonnement d'un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Dict: Informations d'abonnement ou None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                SELECT tier, start_date, end_date, remaining_tokens,
                       total_tokens_used, payment_status, next_payment_date
                FROM subscriptions
                WHERE user_id = ? AND is_active = 1
                ''', (user_id,))
                
                result = cursor.fetchone()
                if result:
                    tier = SubscriptionTier(result[0])
                    features = SubscriptionFeatures.TIERS[tier]
                    
                    return {
                        "tier": tier.value,
                        "features": features,
                        "start_date": result[1],
                        "end_date": result[2],
                        "remaining_tokens": result[3],
                        "total_tokens_used": result[4],
                        "payment_status": result[5],
                        "next_payment_date": result[6]
                    }
                
                return None
                
        except sqlite3.Error:
            return None
    
    def renew_subscription(self, user_id: int) -> bool:
        """
        Renouvelle un abonnement.
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            bool: True si l'abonnement est renouvelé avec succès
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Obtenir les informations actuelles
                cursor = conn.execute('''
                SELECT tier, end_date
                FROM subscriptions
                WHERE user_id = ? AND is_active = 1
                ''', (user_id,))
                
                result = cursor.fetchone()
                if not result:
                    return False
                
                tier = SubscriptionTier(result[0])
                current_end = datetime.fromisoformat(result[1])
                
                # Calculer les nouvelles dates
                new_start = current_end
                new_end = new_start + timedelta(days=30)
                next_payment = new_end - timedelta(days=3)
                
                # Obtenir les nouveaux jetons
                new_tokens = SubscriptionFeatures.TIERS[tier]["tokens_monthly"]
                
                # Mettre à jour l'abonnement
                conn.execute('''
                UPDATE subscriptions
                SET start_date = ?, end_date = ?, next_payment_date = ?,
                    remaining_tokens = remaining_tokens + ?,
                    last_payment_date = ?
                WHERE user_id = ?
                ''', (
                    new_start.isoformat(), new_end.isoformat(),
                    next_payment.isoformat(), new_tokens,
                    datetime.now().isoformat(), user_id
                ))
                
                # Ajouter un bonus de fidélité
                loyalty_bonus = int(new_tokens * 0.05)  # 5% de bonus
                conn.execute('''
                INSERT INTO token_bonuses (
                    user_id, bonus_type, tokens_amount, expiry_date
                ) VALUES (?, ?, ?, ?)
                ''', (
                    user_id, "loyalty_bonus", loyalty_bonus,
                    new_end.isoformat()
                ))
                
                conn.commit()
                return True
                
        except sqlite3.Error:
            return False
