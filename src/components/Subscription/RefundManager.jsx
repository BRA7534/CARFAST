import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    RefreshIcon,
    ExclamationIcon,
    CheckCircleIcon,
    QuestionMarkCircleIcon,
    CashIcon,
    ClockIcon
} from '@heroicons/react/outline';

const RefundManager = ({ refundHistory, onRequestRefund, eligibleTokens }) => {
    const [showRefundModal, setShowRefundModal] = useState(false);
    const [selectedTokens, setSelectedTokens] = useState([]);
    const [reason, setReason] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);

    const handleRefundRequest = async () => {
        setIsProcessing(true);
        try {
            await onRequestRefund({
                tokens: selectedTokens,
                reason,
                timestamp: new Date().toISOString()
            });
            setShowRefundModal(false);
        } catch (error) {
            console.error('Erreur lors de la demande de remboursement:', error);
        }
        setIsProcessing(false);
    };

    const getRefundStatusColor = (status) => {
        switch (status) {
            case 'APPROVED':
                return 'text-green-600 bg-green-100';
            case 'PENDING':
                return 'text-yellow-600 bg-yellow-100';
            case 'REJECTED':
                return 'text-red-600 bg-red-100';
            default:
                return 'text-gray-600 bg-gray-100';
        }
    };

    const getRefundStatusIcon = (status) => {
        switch (status) {
            case 'APPROVED':
                return <CheckCircleIcon className="h-5 w-5" />;
            case 'PENDING':
                return <ClockIcon className="h-5 w-5" />;
            case 'REJECTED':
                return <ExclamationIcon className="h-5 w-5" />;
            default:
                return <QuestionMarkCircleIcon className="h-5 w-5" />;
        }
    };

    return (
        <div className="space-y-6">
            {/* En-tête */}
            <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h3 className="text-lg font-medium text-gray-900">
                            Remboursements
                        </h3>
                        <p className="text-sm text-gray-600">
                            Gérez vos demandes de remboursement de jetons
                        </p>
                    </div>
                    <button
                        onClick={() => setShowRefundModal(true)}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                    >
                        Demander un remboursement
                    </button>
                </div>

                {/* Jetons éligibles */}
                <div className="bg-blue-50 rounded-lg p-4">
                    <div className="flex items-center space-x-3">
                        <CashIcon className="h-5 w-5 text-blue-600" />
                        <div>
                            <div className="font-medium text-blue-900">
                                {eligibleTokens.length} jetons éligibles au remboursement
                            </div>
                            <div className="text-sm text-blue-700">
                                Valeur estimée: {eligibleTokens.length * 0.5}€
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Historique des remboursements */}
            <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Historique des remboursements
                </h3>
                <div className="space-y-4">
                    {refundHistory.map((refund) => (
                        <motion.div
                            key={refund.id}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                        >
                            <div className="flex items-center space-x-4">
                                <div className={`h-10 w-10 rounded-full flex items-center justify-center ${
                                    getRefundStatusColor(refund.status)
                                }`}>
                                    {getRefundStatusIcon(refund.status)}
                                </div>
                                <div>
                                    <div className="font-medium text-gray-900">
                                        {refund.tokens.length} jetons
                                    </div>
                                    <div className="text-sm text-gray-600">
                                        {new Date(refund.timestamp).toLocaleDateString()}
                                    </div>
                                </div>
                            </div>
                            <div className="text-right">
                                <div className="font-medium text-gray-900">
                                    {refund.amount}€
                                </div>
                                <div className={`text-sm ${
                                    getRefundStatusColor(refund.status).split(' ')[0]
                                }`}>
                                    {refund.status}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Modal de demande de remboursement */}
            <AnimatePresence>
                {showRefundModal && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-50 flex items-center justify-center"
                    >
                        <div className="absolute inset-0 bg-black bg-opacity-50" />
                        <div className="relative bg-white rounded-lg p-6 w-full max-w-md">
                            <h3 className="text-lg font-medium text-gray-900 mb-4">
                                Demande de remboursement
                            </h3>

                            <div className="space-y-4">
                                {/* Sélection des jetons */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Jetons à rembourser
                                    </label>
                                    <div className="grid grid-cols-4 gap-2">
                                        {eligibleTokens.map((token) => (
                                            <button
                                                key={token.id}
                                                onClick={() => {
                                                    const isSelected = selectedTokens.includes(token.id);
                                                    setSelectedTokens(
                                                        isSelected
                                                            ? selectedTokens.filter(id => id !== token.id)
                                                            : [...selectedTokens, token.id]
                                                    );
                                                }}
                                                className={`p-2 rounded-lg border ${
                                                    selectedTokens.includes(token.id)
                                                        ? 'border-blue-500 bg-blue-50'
                                                        : 'border-gray-200'
                                                }`}
                                            >
                                                {token.id}
                                            </button>
                                        ))}
                                    </div>
                                </div>

                                {/* Motif */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Motif du remboursement
                                    </label>
                                    <textarea
                                        value={reason}
                                        onChange={(e) => setReason(e.target.value)}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                                        rows={3}
                                        placeholder="Expliquez pourquoi vous souhaitez être remboursé"
                                    />
                                </div>

                                {/* Montant estimé */}
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <div className="flex justify-between items-center">
                                        <span className="text-gray-600">
                                            Montant estimé
                                        </span>
                                        <span className="font-medium text-gray-900">
                                            {selectedTokens.length * 0.5}€
                                        </span>
                                    </div>
                                </div>

                                {/* Actions */}
                                <div className="flex space-x-3">
                                    <button
                                        onClick={() => setShowRefundModal(false)}
                                        className="flex-1 py-2 text-gray-600 hover:text-gray-900"
                                    >
                                        Annuler
                                    </button>
                                    <button
                                        onClick={handleRefundRequest}
                                        disabled={isProcessing || selectedTokens.length === 0 || !reason}
                                        className={`flex-1 py-2 rounded-lg ${
                                            isProcessing || selectedTokens.length === 0 || !reason
                                                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                                : 'bg-blue-600 text-white hover:bg-blue-700'
                                        }`}
                                    >
                                        {isProcessing ? (
                                            <RefreshIcon className="h-5 w-5 animate-spin mx-auto" />
                                        ) : (
                                            'Demander le remboursement'
                                        )}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default RefundManager;
