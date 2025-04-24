import React from 'react';
import { motion } from 'framer-motion';
import { XIcon } from '@heroicons/react/outline';
import { 
    CalendarIcon, 
    SpeedometerIcon, 
    CogIcon,
    ShieldCheckIcon,
    ChartBarIcon,
    DocumentTextIcon,
    LocationMarkerIcon
} from '@heroicons/react/outline';

const VehicleModal = ({ vehicle, onClose }) => {
    // Animation variants
    const modalVariants = {
        hidden: { opacity: 0, scale: 0.8 },
        visible: { opacity: 1, scale: 1 },
        exit: { opacity: 0, scale: 0.8 }
    };

    const overlayVariants = {
        hidden: { opacity: 0 },
        visible: { opacity: 0.5 },
        exit: { opacity: 0 }
    };

    return (
        <div className="fixed inset-0 z-50 overflow-y-auto">
            <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
                {/* Overlay */}
                <motion.div
                    initial="hidden"
                    animate="visible"
                    exit="exit"
                    variants={overlayVariants}
                    className="fixed inset-0 bg-black"
                    onClick={onClose}
                />

                {/* Modal */}
                <motion.div
                    initial="hidden"
                    animate="visible"
                    exit="exit"
                    variants={modalVariants}
                    className="inline-block w-full max-w-4xl my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-lg"
                >
                    {/* En-tête */}
                    <div className="relative">
                        <button
                            onClick={onClose}
                            className="absolute top-4 right-4 text-gray-400 hover:text-gray-500 z-10"
                        >
                            <XIcon className="h-6 w-6" />
                        </button>
                        
                        {/* Galerie d'images */}
                        <div className="relative h-96">
                            <img
                                src={vehicle.image_url || '/placeholder-car.jpg'}
                                alt={`${vehicle.make} ${vehicle.model}`}
                                className="w-full h-full object-cover"
                            />
                            {vehicle.verified && (
                                <div className="absolute top-4 left-4 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-medium">
                                    Vérifié
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Contenu */}
                    <div className="px-6 py-4">
                        <div className="flex justify-between items-start mb-4">
                            <div>
                                <h3 className="text-2xl font-bold text-gray-900">
                                    {vehicle.make} {vehicle.model}
                                </h3>
                                <p className="text-lg text-gray-600">{vehicle.trim}</p>
                            </div>
                            <div className="text-right">
                                <p className="text-3xl font-bold text-blue-600">
                                    {new Intl.NumberFormat('fr-FR', {
                                        style: 'currency',
                                        currency: 'EUR'
                                    }).format(vehicle.price)}
                                </p>
                                {vehicle.price_rating && (
                                    <span className={`text-sm font-medium ${
                                        vehicle.price_rating === 'Bon prix' ? 'text-green-600' : 
                                        vehicle.price_rating === 'Prix élevé' ? 'text-orange-600' : 
                                        'text-gray-600'
                                    }`}>
                                        {vehicle.price_rating}
                                    </span>
                                )}
                            </div>
                        </div>

                        {/* Caractéristiques principales */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                            <div className="flex items-center space-x-2">
                                <CalendarIcon className="h-5 w-5 text-gray-400" />
                                <span className="text-gray-600">{vehicle.year}</span>
                            </div>
                            <div className="flex items-center space-x-2">
                                <SpeedometerIcon className="h-5 w-5 text-gray-400" />
                                <span className="text-gray-600">
                                    {vehicle.mileage.toLocaleString()} km
                                </span>
                            </div>
                            <div className="flex items-center space-x-2">
                                <CogIcon className="h-5 w-5 text-gray-400" />
                                <span className="text-gray-600">{vehicle.transmission}</span>
                            </div>
                            <div className="flex items-center space-x-2">
                                <LocationMarkerIcon className="h-5 w-5 text-gray-400" />
                                <span className="text-gray-600">{vehicle.location}</span>
                            </div>
                        </div>

                        {/* Onglets d'information */}
                        <div className="border-t border-gray-200 pt-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {/* Spécifications techniques */}
                                <div>
                                    <h4 className="text-lg font-semibold mb-4 flex items-center">
                                        <DocumentTextIcon className="h-5 w-5 mr-2" />
                                        Spécifications
                                    </h4>
                                    <dl className="space-y-2">
                                        {Object.entries(vehicle.specifications || {}).map(([key, value]) => (
                                            <div key={key} className="flex justify-between">
                                                <dt className="text-gray-600">{key}</dt>
                                                <dd className="font-medium">{value}</dd>
                                            </div>
                                        ))}
                                    </dl>
                                </div>

                                {/* Sécurité et performances */}
                                <div>
                                    <h4 className="text-lg font-semibold mb-4 flex items-center">
                                        <ShieldCheckIcon className="h-5 w-5 mr-2" />
                                        Sécurité et performances
                                    </h4>
                                    <div className="space-y-4">
                                        <div>
                                            <div className="flex justify-between items-center mb-1">
                                                <span className="text-sm text-gray-600">
                                                    Note de sécurité
                                                </span>
                                                <span className="font-medium">
                                                    {vehicle.safety_rating}/5
                                                </span>
                                            </div>
                                            <div className="h-2 bg-gray-200 rounded-full">
                                                <div
                                                    className="h-2 bg-green-500 rounded-full"
                                                    style={{
                                                        width: `${(vehicle.safety_rating / 5) * 100}%`
                                                    }}
                                                />
                                            </div>
                                        </div>
                                        
                                        {vehicle.performance_metrics?.map((metric) => (
                                            <div key={metric.name}>
                                                <div className="flex justify-between items-center mb-1">
                                                    <span className="text-sm text-gray-600">
                                                        {metric.name}
                                                    </span>
                                                    <span className="font-medium">
                                                        {metric.value}
                                                    </span>
                                                </div>
                                                <div className="h-2 bg-gray-200 rounded-full">
                                                    <div
                                                        className="h-2 bg-blue-500 rounded-full"
                                                        style={{
                                                            width: `${metric.percentage}%`
                                                        }}
                                                    />
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Boutons d'action */}
                        <div className="mt-6 flex space-x-4">
                            <button className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium">
                                Contacter le vendeur
                            </button>
                            <button className="flex-1 border border-blue-600 text-blue-600 px-6 py-3 rounded-lg hover:bg-blue-50 transition-colors font-medium">
                                Sauvegarder
                            </button>
                        </div>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default VehicleModal;
