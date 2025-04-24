import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
    DocumentSearchIcon,
    ExclamationIcon,
    CheckCircleIcon,
    ClockIcon,
    ShieldCheckIcon
} from '@heroicons/react/outline';

const HistoVecIntegration = ({ onVehicleDataReceived }) => {
    const [formData, setFormData] = useState({
        immatriculation: '',
        formule: '',
        dateImmatriculation: ''
    });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [vehicleData, setVehicleData] = useState(null);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value.toUpperCase()
        }));
    };

    const formatImmatriculation = (immat) => {
        // Format AA-123-AA
        return immat.replace(/[^A-Z0-9]/g, '').replace(/(\w{2})(\d{3})(\w{2})/, '$1-$2-$3');
    };

    const validateForm = () => {
        if (!formData.immatriculation || !formData.formule || !formData.dateImmatriculation) {
            setError('Tous les champs sont obligatoires');
            return false;
        }
        return true;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        if (!validateForm()) return;

        setIsLoading(true);
        try {
            // Simulation d'appel à l'API HistoVec (à remplacer par l'API réelle)
            const response = await fetch('https://histovec.interieur.gouv.fr/api/v1/report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    plaque: formatImmatriculation(formData.immatriculation),
                    formule: formData.formule,
                    date_immatriculation: formData.dateImmatriculation
                })
            });

            if (!response.ok) throw new Error('Erreur lors de la récupération des données');

            const data = await response.json();
            setVehicleData(data);
            onVehicleDataReceived(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const renderVehicleInfo = () => {
        if (!vehicleData) return null;

        return (
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6 bg-white rounded-lg shadow-sm p-6"
            >
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Informations du véhicule
                </h3>

                <div className="space-y-4">
                    {/* Caractéristiques techniques */}
                    <div className="border-b pb-4">
                        <h4 className="text-sm font-medium text-gray-700 mb-2">
                            Caractéristiques techniques
                        </h4>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <span className="text-sm text-gray-500">Marque</span>
                                <p className="font-medium text-gray-900">{vehicleData.marque}</p>
                            </div>
                            <div>
                                <span className="text-sm text-gray-500">Modèle</span>
                                <p className="font-medium text-gray-900">{vehicleData.modele}</p>
                            </div>
                            <div>
                                <span className="text-sm text-gray-500">Année</span>
                                <p className="font-medium text-gray-900">{vehicleData.annee}</p>
                            </div>
                            <div>
                                <span className="text-sm text-gray-500">Puissance</span>
                                <p className="font-medium text-gray-900">{vehicleData.puissance} CV</p>
                            </div>
                        </div>
                    </div>

                    {/* Historique */}
                    <div className="border-b pb-4">
                        <h4 className="text-sm font-medium text-gray-700 mb-2">
                            Historique
                        </h4>
                        <div className="space-y-3">
                            {vehicleData.historique?.map((event, index) => (
                                <div key={index} className="flex items-start space-x-3">
                                    <div className="flex-shrink-0">
                                        <ClockIcon className="h-5 w-5 text-gray-400" />
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-gray-900">
                                            {event.type}
                                        </p>
                                        <p className="text-sm text-gray-500">
                                            {event.date}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Situation administrative */}
                    <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-2">
                            Situation administrative
                        </h4>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="flex items-center space-x-2">
                                <ShieldCheckIcon className="h-5 w-5 text-green-500" />
                                <span className="text-sm text-gray-900">
                                    {vehicleData.situation.vol ? 'Volé' : 'Non volé'}
                                </span>
                            </div>
                            <div className="flex items-center space-x-2">
                                <ShieldCheckIcon className="h-5 w-5 text-green-500" />
                                <span className="text-sm text-gray-900">
                                    {vehicleData.situation.gage ? 'Gagé' : 'Non gagé'}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </motion.div>
        );
    };

    return (
        <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex items-center space-x-3 mb-6">
                    <DocumentSearchIcon className="h-6 w-6 text-blue-600" />
                    <h2 className="text-lg font-medium text-gray-900">
                        Vérification HistoVec
                    </h2>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Immatriculation
                        </label>
                        <input
                            type="text"
                            name="immatriculation"
                            value={formData.immatriculation}
                            onChange={handleInputChange}
                            placeholder="AA-123-AA"
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Numéro de formule
                        </label>
                        <input
                            type="text"
                            name="formule"
                            value={formData.formule}
                            onChange={handleInputChange}
                            placeholder="2013AB12345"
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Date d'immatriculation
                        </label>
                        <input
                            type="date"
                            name="dateImmatriculation"
                            value={formData.dateImmatriculation}
                            onChange={handleInputChange}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    {error && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="flex items-center space-x-2 text-red-600"
                        >
                            <ExclamationIcon className="h-5 w-5" />
                            <span className="text-sm">{error}</span>
                        </motion.div>
                    )}

                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full py-3 px-4 rounded-lg flex items-center justify-center space-x-2 ${
                            isLoading
                                ? 'bg-gray-100 cursor-not-allowed'
                                : 'bg-blue-600 hover:bg-blue-700'
                        } text-white font-medium`}
                    >
                        {isLoading ? (
                            <>
                                <ClockIcon className="h-5 w-5 animate-spin" />
                                <span>Vérification en cours...</span>
                            </>
                        ) : (
                            <>
                                <DocumentSearchIcon className="h-5 w-5" />
                                <span>Vérifier le véhicule</span>
                            </>
                        )}
                    </button>
                </form>
            </div>

            {renderVehicleInfo()}
        </div>
    );
};

export default HistoVecIntegration;
