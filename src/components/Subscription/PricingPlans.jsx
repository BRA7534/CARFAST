import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckIcon, XIcon } from '@heroicons/react/outline';

const PricingPlans = ({ onSelectPlan }) => {
    const [billingCycle, setBillingCycle] = useState('monthly');
    const [selectedPlan, setSelectedPlan] = useState(null);

    const plans = [
        {
            id: 'free_trial',
            name: 'Essai Gratuit',
            description: 'Testez CarFast pendant 7 jours',
            price: {
                monthly: 0,
                annually: 0
            },
            features: [
                '3 recherches de véhicules',
                'Informations de base',
                '5 jetons d\'essai'
            ],
            tokenAmount: 5,
            popular: false,
            trial: true
        },
        {
            id: 'basic',
            name: 'Basic',
            description: 'Idéal pour les particuliers',
            price: {
                monthly: 9.99,
                annually: 99.99
            },
            features: [
                '20 recherches par mois',
                'Historique complet',
                'Rapports de base',
                '20 jetons mensuels'
            ],
            tokenAmount: 20,
            popular: false
        },
        {
            id: 'pro',
            name: 'Pro',
            description: 'Pour les passionnés d\'automobile',
            price: {
                monthly: 19.99,
                annually: 199.99
            },
            features: [
                'Recherches illimitées',
                'Historique détaillé',
                'Rapports professionnels',
                'Comparaison de véhicules',
                '50 jetons mensuels'
            ],
            tokenAmount: 50,
            popular: true
        },
        {
            id: 'premium',
            name: 'Premium',
            description: 'Notre meilleure offre',
            price: {
                monthly: 29.99,
                annually: 299.99
            },
            features: [
                'Tout inclus',
                'Accès API',
                'Support prioritaire',
                'Jetons illimités'
            ],
            tokenAmount: 'Illimité',
            popular: false
        }
    ];

    return (
        <div className="py-12 bg-gray-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* En-tête */}
                <div className="text-center mb-12">
                    <motion.h2
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-3xl font-bold text-gray-900 mb-4"
                    >
                        Choisissez votre formule
                    </motion.h2>
                    <p className="text-xl text-gray-600">
                        Commencez gratuitement et évoluez selon vos besoins
                    </p>
                </div>

                {/* Sélecteur de cycle de facturation */}
                <div className="flex justify-center mb-12">
                    <div className="relative bg-white rounded-lg p-1 flex">
                        <button
                            onClick={() => setBillingCycle('monthly')}
                            className={`px-4 py-2 text-sm font-medium rounded-md ${
                                billingCycle === 'monthly'
                                    ? 'bg-blue-600 text-white'
                                    : 'text-gray-700 hover:text-gray-900'
                            }`}
                        >
                            Mensuel
                        </button>
                        <button
                            onClick={() => setBillingCycle('annually')}
                            className={`px-4 py-2 text-sm font-medium rounded-md ${
                                billingCycle === 'annually'
                                    ? 'bg-blue-600 text-white'
                                    : 'text-gray-700 hover:text-gray-900'
                            }`}
                        >
                            Annuel
                            <span className="ml-1 text-xs text-green-500">
                                -20%
                            </span>
                        </button>
                    </div>
                </div>

                {/* Grille des plans */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <AnimatePresence>
                        {plans.map((plan) => (
                            <motion.div
                                key={plan.id}
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                whileHover={{ scale: 1.02 }}
                                className={`relative bg-white rounded-2xl shadow-lg overflow-hidden ${
                                    plan.popular
                                        ? 'border-2 border-blue-500'
                                        : 'border border-gray-200'
                                }`}
                            >
                                {plan.popular && (
                                    <div className="absolute top-0 right-0 bg-blue-500 text-white px-4 py-1 text-sm font-medium">
                                        Populaire
                                    </div>
                                )}

                                <div className="p-6">
                                    <h3 className="text-xl font-bold text-gray-900 mb-2">
                                        {plan.name}
                                    </h3>
                                    <p className="text-gray-600 mb-4">
                                        {plan.description}
                                    </p>

                                    <div className="mb-6">
                                        <div className="flex items-baseline">
                                            <span className="text-4xl font-bold text-gray-900">
                                                {plan.price[billingCycle]}€
                                            </span>
                                            <span className="ml-2 text-gray-500">
                                                /{billingCycle === 'monthly' ? 'mois' : 'an'}
                                            </span>
                                        </div>
                                        <div className="mt-1 text-sm text-gray-500">
                                            {plan.tokenAmount} jetons inclus
                                        </div>
                                    </div>

                                    <button
                                        onClick={() => {
                                            setSelectedPlan(plan.id);
                                            onSelectPlan(plan);
                                        }}
                                        className={`w-full py-3 px-4 rounded-lg font-medium ${
                                            plan.trial
                                                ? 'bg-green-600 hover:bg-green-700 text-white'
                                                : plan.popular
                                                ? 'bg-blue-600 hover:bg-blue-700 text-white'
                                                : 'bg-gray-100 hover:bg-gray-200 text-gray-900'
                                        }`}
                                    >
                                        {plan.trial ? 'Commencer l\'essai gratuit' : 'Choisir ce plan'}
                                    </button>

                                    <ul className="mt-6 space-y-4">
                                        {plan.features.map((feature, index) => (
                                            <li
                                                key={index}
                                                className="flex items-start"
                                            >
                                                <CheckIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0" />
                                                <span className="text-gray-600">
                                                    {feature}
                                                </span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </div>

                {/* Section FAQ */}
                <div className="mt-16">
                    <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">
                        Questions fréquentes
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div className="bg-white rounded-lg p-6">
                            <h4 className="font-medium text-gray-900 mb-2">
                                Comment fonctionnent les jetons ?
                            </h4>
                            <p className="text-gray-600">
                                Les jetons vous permettent d'accéder aux fonctionnalités premium 
                                comme les rapports détaillés ou la comparaison de véhicules. 
                                Chaque action consomme un certain nombre de jetons.
                            </p>
                        </div>
                        <div className="bg-white rounded-lg p-6">
                            <h4 className="font-medium text-gray-900 mb-2">
                                Puis-je changer de plan ?
                            </h4>
                            <p className="text-gray-600">
                                Oui, vous pouvez changer de plan à tout moment. Les jetons 
                                restants seront transférés vers votre nouveau plan.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PricingPlans;
