import React from 'react';
import { motion } from 'framer-motion';
import {
    CurrencyDollarIcon,
    LightningBoltIcon,
    ExclamationIcon,
    InformationCircleIcon
} from '@heroicons/react/outline';

const TokenManager = ({ tokens, onPurchaseTokens, onUseTokens }) => {
    const tokenPackages = [
        {
            id: 'small',
            amount: 10,
            price: 4.99,
            popular: false
        },
        {
            id: 'medium',
            amount: 25,
            price: 9.99,
            popular: true
        },
        {
            id: 'large',
            amount: 50,
            price: 14.99,
            popular: false
        }
    ];

    const tokenUsage = {
        'Recherche de véhicule': 1,
        'Rapport détaillé': 2,
        'Historique complet': 3,
        'Comparaison de véhicules': 2,
        'Export PDF': 1
    };

    return (
        <div className="bg-white rounded-lg shadow-lg p-6">
            {/* Solde de jetons */}
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        Vos jetons
                    </h2>
                    <p className="text-gray-600">
                        Utilisez vos jetons pour accéder aux fonctionnalités premium
                    </p>
                </div>
                <div className="bg-blue-50 px-6 py-3 rounded-lg">
                    <div className="text-sm text-blue-600 mb-1">Solde actuel</div>
                    <div className="text-3xl font-bold text-blue-700">
                        {tokens} <span className="text-sm font-normal">jetons</span>
                    </div>
                </div>
            </div>

            {/* Alerte si solde bas */}
            {tokens < 5 && (
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-8"
                >
                    <div className="flex items-center">
                        <ExclamationIcon className="h-5 w-5 text-yellow-400 mr-2" />
                        <p className="text-sm text-yellow-700">
                            Votre solde de jetons est bas. Pensez à recharger pour 
                            continuer à profiter de toutes les fonctionnalités.
                        </p>
                    </div>
                </motion.div>
            )}

            {/* Acheter des jetons */}
            <div className="mb-8">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Recharger des jetons
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {tokenPackages.map((pkg) => (
                        <motion.div
                            key={pkg.id}
                            whileHover={{ scale: 1.02 }}
                            className={`relative border rounded-lg p-4 ${
                                pkg.popular
                                    ? 'border-blue-500 bg-blue-50'
                                    : 'border-gray-200'
                            }`}
                        >
                            {pkg.popular && (
                                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                                    <span className="bg-blue-500 text-white text-xs px-2 py-1 rounded-full">
                                        Meilleure offre
                                    </span>
                                </div>
                            )}
                            <div className="text-center mb-4">
                                <div className="text-2xl font-bold text-gray-900">
                                    {pkg.amount} jetons
                                </div>
                                <div className="text-gray-600">
                                    {pkg.price}€
                                </div>
                                <div className="text-sm text-green-600">
                                    {(pkg.price / pkg.amount).toFixed(2)}€ par jeton
                                </div>
                            </div>
                            <button
                                onClick={() => onPurchaseTokens(pkg)}
                                className={`w-full py-2 rounded-lg font-medium ${
                                    pkg.popular
                                        ? 'bg-blue-600 hover:bg-blue-700 text-white'
                                        : 'bg-gray-100 hover:bg-gray-200 text-gray-900'
                                }`}
                            >
                                Acheter
                            </button>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Utilisation des jetons */}
            <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Coût en jetons par fonctionnalité
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.entries(tokenUsage).map(([feature, cost]) => (
                        <div
                            key={feature}
                            className="flex items-center justify-between border border-gray-200 rounded-lg p-4"
                        >
                            <div className="flex items-center">
                                <LightningBoltIcon className="h-5 w-5 text-yellow-500 mr-2" />
                                <span className="text-gray-900">{feature}</span>
                            </div>
                            <div className="flex items-center">
                                <span className="font-medium text-gray-900">
                                    {cost} {cost === 1 ? 'jeton' : 'jetons'}
                                </span>
                                <button
                                    onClick={() => onUseTokens(feature, cost)}
                                    className={`ml-4 px-3 py-1 rounded-lg text-sm font-medium ${
                                        tokens >= cost
                                            ? 'bg-green-100 text-green-700 hover:bg-green-200'
                                            : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                    }`}
                                    disabled={tokens < cost}
                                >
                                    Utiliser
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Note d'information */}
            <div className="mt-8 bg-gray-50 rounded-lg p-4">
                <div className="flex items-start">
                    <InformationCircleIcon className="h-5 w-5 text-gray-400 mr-2 flex-shrink-0" />
                    <p className="text-sm text-gray-600">
                        Les jetons non utilisés restent valables pendant 12 mois à 
                        compter de leur date d'achat. Pour plus d'économies, 
                        pensez à souscrire à un abonnement qui inclut des jetons 
                        mensuels.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default TokenManager;
