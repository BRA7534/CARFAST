import React from 'react';
import { motion } from 'framer-motion';
import {
    StarIcon,
    ChartBarIcon,
    GiftIcon,
    TrendingUpIcon,
    ClockIcon
} from '@heroicons/react/outline';

const LoyaltyProgram = ({ loyalty, onRedeemPoints }) => {
    const tiers = [
        {
            name: 'BRONZE',
            minPoints: 0,
            color: 'from-yellow-700 to-yellow-900',
            textColor: 'text-yellow-800'
        },
        {
            name: 'SILVER',
            minPoints: 1000,
            color: 'from-gray-300 to-gray-400',
            textColor: 'text-gray-600'
        },
        {
            name: 'GOLD',
            minPoints: 5000,
            color: 'from-yellow-400 to-yellow-500',
            textColor: 'text-yellow-600'
        },
        {
            name: 'PLATINUM',
            minPoints: 10000,
            color: 'from-blue-400 to-blue-600',
            textColor: 'text-blue-600'
        }
    ];

    const getCurrentTier = (points) => {
        return tiers
            .slice()
            .reverse()
            .find((tier) => points >= tier.minPoints);
    };

    const getNextTier = (points) => {
        return tiers.find((tier) => points < tier.minPoints);
    };

    const currentTier = getCurrentTier(loyalty.points);
    const nextTier = getNextTier(loyalty.points);
    const progress = nextTier
        ? ((loyalty.points - currentTier.minPoints) /
          (nextTier.minPoints - currentTier.minPoints)) *
          100
        : 100;

    return (
        <div className="space-y-6">
            {/* Carte de statut */}
            <div className={`bg-gradient-to-r ${currentTier.color} p-6 rounded-lg text-white`}>
                <div className="flex justify-between items-start mb-4">
                    <div>
                        <h3 className="text-2xl font-bold mb-1">
                            Statut {currentTier.name}
                        </h3>
                        <p className="text-white/80">
                            {loyalty.points} points de fidélité
                        </p>
                    </div>
                    <div className="h-12 w-12 rounded-full bg-white/20 flex items-center justify-center">
                        <StarIcon className="h-6 w-6 text-white" />
                    </div>
                </div>

                {nextTier && (
                    <div>
                        <div className="flex justify-between text-sm mb-2">
                            <span>Progression vers {nextTier.name}</span>
                            <span>{Math.round(progress)}%</span>
                        </div>
                        <div className="h-2 bg-white/20 rounded-full">
                            <div
                                className="h-2 bg-white rounded-full transition-all duration-500"
                                style={{ width: `${progress}%` }}
                            />
                        </div>
                        <p className="text-sm mt-2">
                            {nextTier.minPoints - loyalty.points} points pour le prochain niveau
                        </p>
                    </div>
                )}
            </div>

            {/* Avantages du niveau */}
            <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Vos avantages actuels
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {loyalty.benefits.map((benefit) => (
                        <motion.div
                            key={benefit.id}
                            whileHover={{ scale: 1.02 }}
                            className="p-4 border border-gray-200 rounded-lg"
                        >
                            <div className="flex items-start">
                                <div className="h-8 w-8 rounded-lg bg-blue-100 flex items-center justify-center mr-3">
                                    {benefit.type === 'TOKEN_MULTIPLIER' && (
                                        <TrendingUpIcon className="h-5 w-5 text-blue-600" />
                                    )}
                                    {benefit.type === 'DISCOUNT_PERCENTAGE' && (
                                        <GiftIcon className="h-5 w-5 text-blue-600" />
                                    )}
                                    {benefit.type === 'FREE_TOKENS' && (
                                        <StarIcon className="h-5 w-5 text-blue-600" />
                                    )}
                                    {benefit.type === 'EXTENDED_VALIDITY' && (
                                        <ClockIcon className="h-5 w-5 text-blue-600" />
                                    )}
                                </div>
                                <div>
                                    <h4 className="font-medium text-gray-900">
                                        {benefit.name}
                                    </h4>
                                    <p className="text-sm text-gray-600">
                                        {benefit.description}
                                    </p>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Historique des points */}
            <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Historique des points
                </h3>
                <div className="space-y-4">
                    {loyalty.pointsHistory.map((transaction) => (
                        <motion.div
                            key={transaction.id}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                        >
                            <div className="flex items-center">
                                <ChartBarIcon className={`h-5 w-5 mr-3 ${
                                    transaction.type === 'EARNED'
                                        ? 'text-green-500'
                                        : transaction.type === 'REDEEMED'
                                        ? 'text-blue-500'
                                        : 'text-red-500'
                                }`} />
                                <div>
                                    <p className="text-sm font-medium text-gray-900">
                                        {transaction.description}
                                    </p>
                                    <p className="text-xs text-gray-500">
                                        {new Date(transaction.timestamp).toLocaleDateString()}
                                    </p>
                                </div>
                            </div>
                            <span className={`font-medium ${
                                transaction.type === 'EARNED'
                                    ? 'text-green-600'
                                    : transaction.type === 'REDEEMED'
                                    ? 'text-blue-600'
                                    : 'text-red-600'
                            }`}>
                                {transaction.type === 'EARNED' ? '+' : '-'}
                                {transaction.points} points
                            </span>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Récompenses disponibles */}
            <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg font-medium text-gray-900">
                        Récompenses disponibles
                    </h3>
                    <span className="text-sm text-gray-600">
                        {loyalty.points} points disponibles
                    </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {[
                        {
                            id: 'reward1',
                            name: '10 jetons gratuits',
                            points: 500,
                            description: 'Échangez vos points contre des jetons'
                        },
                        {
                            id: 'reward2',
                            name: 'Réduction de 20%',
                            points: 1000,
                            description: 'Sur votre prochain abonnement'
                        },
                        {
                            id: 'reward3',
                            name: 'Accès Premium 1 mois',
                            points: 2000,
                            description: 'Essayez toutes les fonctionnalités premium'
                        }
                    ].map((reward) => (
                        <motion.div
                            key={reward.id}
                            whileHover={{ scale: 1.02 }}
                            className="border border-gray-200 rounded-lg p-4"
                        >
                            <div className="flex justify-between items-start mb-2">
                                <h4 className="font-medium text-gray-900">
                                    {reward.name}
                                </h4>
                                <span className="text-sm font-medium text-blue-600">
                                    {reward.points} pts
                                </span>
                            </div>
                            <p className="text-sm text-gray-600 mb-4">
                                {reward.description}
                            </p>
                            <button
                                onClick={() => onRedeemPoints(reward)}
                                disabled={loyalty.points < reward.points}
                                className={`w-full py-2 rounded-lg text-sm font-medium ${
                                    loyalty.points >= reward.points
                                        ? 'bg-blue-600 hover:bg-blue-700 text-white'
                                        : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                }`}
                            >
                                Échanger
                            </button>
                        </motion.div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default LoyaltyProgram;
