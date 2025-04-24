import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    TagIcon,
    GiftIcon,
    ClockIcon,
    CheckCircleIcon,
    XCircleIcon
} from '@heroicons/react/outline';

const PromotionManager = ({ activePromotions, onApplyPromotion }) => {
    const [promoCode, setPromoCode] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleApplyPromo = async () => {
        setError(null);
        setSuccess(null);
        
        try {
            const result = await onApplyPromotion(promoCode);
            setSuccess('Code promo appliqué avec succès !');
            setPromoCode('');
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="space-y-6">
            {/* Section d'application du code promo */}
            <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Appliquer un code promo
                </h3>
                <div className="flex space-x-4">
                    <div className="flex-1">
                        <div className="relative">
                            <TagIcon className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                            <input
                                type="text"
                                value={promoCode}
                                onChange={(e) => setPromoCode(e.target.value.toUpperCase())}
                                placeholder="Entrez votre code promo"
                                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            />
                        </div>
                    </div>
                    <button
                        onClick={handleApplyPromo}
                        disabled={!promoCode}
                        className={`px-6 py-2 rounded-lg font-medium ${
                            promoCode
                                ? 'bg-blue-600 hover:bg-blue-700 text-white'
                                : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        }`}
                    >
                        Appliquer
                    </button>
                </div>

                <AnimatePresence>
                    {error && (
                        <motion.div
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0 }}
                            className="flex items-center mt-3 text-red-600"
                        >
                            <XCircleIcon className="h-5 w-5 mr-2" />
                            <span className="text-sm">{error}</span>
                        </motion.div>
                    )}
                    {success && (
                        <motion.div
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0 }}
                            className="flex items-center mt-3 text-green-600"
                        >
                            <CheckCircleIcon className="h-5 w-5 mr-2" />
                            <span className="text-sm">{success}</span>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* Promotions actives */}
            {activePromotions?.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Promotions actives
                    </h3>
                    <div className="space-y-4">
                        {activePromotions.map((promo) => (
                            <motion.div
                                key={promo.id}
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="flex items-start p-4 bg-blue-50 rounded-lg"
                            >
                                <GiftIcon className="h-6 w-6 text-blue-600 mr-4 flex-shrink-0" />
                                <div className="flex-1">
                                    <div className="flex items-center justify-between">
                                        <h4 className="font-medium text-gray-900">
                                            {promo.description}
                                        </h4>
                                        <span className="text-sm text-blue-600 font-medium">
                                            {promo.code}
                                        </span>
                                    </div>
                                    <div className="mt-1 text-sm text-gray-600">
                                        {promo.type === 'PERCENTAGE_OFF' && `${promo.value}% de réduction`}
                                        {promo.type === 'FIXED_AMOUNT_OFF' && `${promo.value}€ de réduction`}
                                        {promo.type === 'FREE_TOKENS' && `${promo.value} jetons gratuits`}
                                        {promo.type === 'EXTENDED_TRIAL' && `${promo.value} jours d'essai supplémentaires`}
                                    </div>
                                    <div className="mt-2 flex items-center text-sm text-gray-500">
                                        <ClockIcon className="h-4 w-4 mr-1" />
                                        <span>
                                            Expire le {new Date(promo.endDate).toLocaleDateString()}
                                        </span>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            )}

            {/* Offres spéciales */}
            <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg shadow-lg p-6 text-white">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium">Offre spéciale</h3>
                    <span className="px-3 py-1 bg-white text-purple-600 rounded-full text-sm font-medium">
                        Limité
                    </span>
                </div>
                <p className="text-lg mb-4">
                    Parrainez un ami et recevez chacun 20 jetons gratuits !
                </p>
                <button className="w-full bg-white text-purple-600 px-6 py-2 rounded-lg font-medium hover:bg-gray-100 transition-colors">
                    Parrainer maintenant
                </button>
            </div>
        </div>
    );
};

export default PromotionManager;
