import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    CreditCardIcon,
    LockClosedIcon,
    ExclamationIcon,
    DocumentTextIcon,
    RefreshIcon,
    CheckCircleIcon
} from '@heroicons/react/outline';
import { loadStripe } from '@stripe/stripe-js';
import { CardElement, Elements, useStripe, useElements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLIC_KEY);

const PaymentForm = ({ onSubmit, isProcessing }) => {
    const stripe = useStripe();
    const elements = useElements();
    const [error, setError] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);

        if (!stripe || !elements) {
            return;
        }

        const { error: stripeError, paymentMethod } = await stripe.createPaymentMethod({
            type: 'card',
            card: elements.getElement(CardElement),
        });

        if (stripeError) {
            setError(stripeError.message);
            return;
        }

        onSubmit(paymentMethod);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div className="bg-gray-50 rounded-lg p-4">
                <CardElement
                    options={{
                        style: {
                            base: {
                                fontSize: '16px',
                                color: '#424770',
                                '::placeholder': {
                                    color: '#aab7c4',
                                },
                            },
                            invalid: {
                                color: '#9e2146',
                            },
                        },
                    }}
                />
            </div>

            {error && (
                <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-center text-red-600 text-sm"
                >
                    <ExclamationIcon className="h-5 w-5 mr-2" />
                    {error}
                </motion.div>
            )}

            <button
                type="submit"
                disabled={!stripe || isProcessing}
                className={`w-full py-3 px-4 rounded-lg flex items-center justify-center space-x-2 ${
                    isProcessing
                        ? 'bg-gray-100 cursor-not-allowed'
                        : 'bg-blue-600 hover:bg-blue-700'
                } text-white font-medium`}
            >
                <LockClosedIcon className="h-5 w-5" />
                <span>
                    {isProcessing ? 'Traitement...' : 'Payer en toute sécurité'}
                </span>
            </button>
        </form>
    );
};

const PaymentManager = ({
    subscription,
    paymentHistory,
    onUpdatePayment,
    onCancelSubscription
}) => {
    const [showUpdateCard, setShowUpdateCard] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);

    const handlePaymentUpdate = async (paymentMethod) => {
        setIsProcessing(true);
        try {
            await onUpdatePayment(paymentMethod);
            setShowUpdateCard(false);
        } catch (error) {
            console.error('Erreur lors de la mise à jour du paiement:', error);
        }
        setIsProcessing(false);
    };

    return (
        <div className="space-y-6">
            {/* Informations de paiement actuelles */}
            <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-medium text-gray-900">
                        Mode de paiement
                    </h3>
                    <button
                        onClick={() => setShowUpdateCard(true)}
                        className="text-blue-600 hover:text-blue-700 font-medium"
                    >
                        Mettre à jour
                    </button>
                </div>

                <div className="flex items-center space-x-4">
                    <div className="h-12 w-12 bg-gray-100 rounded-lg flex items-center justify-center">
                        <CreditCardIcon className="h-6 w-6 text-gray-600" />
                    </div>
                    <div>
                        <div className="font-medium text-gray-900">
                            •••• •••• •••• {subscription.paymentMethod?.lastFour}
                        </div>
                        <div className="text-sm text-gray-600">
                            Expire le {subscription.paymentMethod?.expiryDate}
                        </div>
                    </div>
                </div>
            </div>

            {/* Modal de mise à jour de la carte */}
            <AnimatePresence>
                {showUpdateCard && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-50 flex items-center justify-center"
                    >
                        <div className="absolute inset-0 bg-black bg-opacity-50" />
                        <div className="relative bg-white rounded-lg p-6 w-full max-w-md">
                            <h3 className="text-lg font-medium text-gray-900 mb-4">
                                Mettre à jour le mode de paiement
                            </h3>
                            <Elements stripe={stripePromise}>
                                <PaymentForm
                                    onSubmit={handlePaymentUpdate}
                                    isProcessing={isProcessing}
                                />
                            </Elements>
                            <button
                                onClick={() => setShowUpdateCard(false)}
                                className="mt-4 w-full py-2 text-gray-600 hover:text-gray-900"
                            >
                                Annuler
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Détails de l'abonnement */}
            <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Détails de l'abonnement
                </h3>
                <div className="space-y-4">
                    <div className="flex justify-between items-center py-3 border-b">
                        <div className="text-gray-600">Plan</div>
                        <div className="font-medium text-gray-900">
                            {subscription.plan}
                        </div>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b">
                        <div className="text-gray-600">Prix</div>
                        <div className="font-medium text-gray-900">
                            {subscription.price}€/{subscription.interval}
                        </div>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b">
                        <div className="text-gray-600">Prochain paiement</div>
                        <div className="font-medium text-gray-900">
                            {new Date(subscription.nextBillingDate).toLocaleDateString()}
                        </div>
                    </div>
                    <div className="flex justify-between items-center py-3">
                        <div className="text-gray-600">Renouvellement automatique</div>
                        <div className="font-medium text-gray-900">
                            {subscription.autoRenew ? 'Activé' : 'Désactivé'}
                        </div>
                    </div>
                </div>

                <button
                    onClick={onCancelSubscription}
                    className="mt-6 w-full py-2 text-red-600 hover:text-red-700 font-medium"
                >
                    Annuler l'abonnement
                </button>
            </div>

            {/* Historique des paiements */}
            <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Historique des paiements
                </h3>
                <div className="space-y-4">
                    {paymentHistory.map((payment) => (
                        <div
                            key={payment.id}
                            className="flex items-center justify-between py-3 border-b last:border-0"
                        >
                            <div className="flex items-center space-x-4">
                                <div className={`h-8 w-8 rounded-full flex items-center justify-center ${
                                    payment.status === 'SUCCESS'
                                        ? 'bg-green-100 text-green-600'
                                        : 'bg-red-100 text-red-600'
                                }`}>
                                    {payment.status === 'SUCCESS' ? (
                                        <CheckCircleIcon className="h-5 w-5" />
                                    ) : (
                                        <ExclamationIcon className="h-5 w-5" />
                                    )}
                                </div>
                                <div>
                                    <div className="font-medium text-gray-900">
                                        {payment.amount}€
                                    </div>
                                    <div className="text-sm text-gray-600">
                                        {new Date(payment.date).toLocaleDateString()}
                                    </div>
                                </div>
                            </div>
                            <button
                                onClick={() => window.open(payment.receiptUrl, '_blank')}
                                className="text-blue-600 hover:text-blue-700"
                            >
                                <DocumentTextIcon className="h-5 w-5" />
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default PaymentManager;
