import React from 'react';
import { motion } from 'framer-motion';
import { 
    CalendarIcon, 
    SpeedometerIcon, 
    FuelIcon, 
    ShieldCheckIcon,
    StarIcon 
} from '@heroicons/react/outline';

const VehicleCard = ({ vehicle, onClick }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            whileHover={{ scale: 1.02 }}
            className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer"
            onClick={() => onClick(vehicle)}
        >
            {/* Image du véhicule */}
            <div className="relative h-48 w-full">
                <img
                    src={vehicle.image_url || '/placeholder-car.jpg'}
                    alt={`${vehicle.make} ${vehicle.model}`}
                    className="w-full h-full object-cover"
                />
                {vehicle.verified && (
                    <div className="absolute top-2 right-2 bg-green-500 text-white px-2 py-1 rounded-full text-xs font-medium">
                        Vérifié
                    </div>
                )}
            </div>

            {/* Informations principales */}
            <div className="p-4">
                <div className="flex justify-between items-start mb-2">
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900">
                            {vehicle.make} {vehicle.model}
                        </h3>
                        <p className="text-sm text-gray-600">{vehicle.trim}</p>
                    </div>
                    <div className="flex items-center">
                        <StarIcon className="h-5 w-5 text-yellow-400" />
                        <span className="ml-1 text-sm font-medium text-gray-700">
                            {vehicle.rating}
                        </span>
                    </div>
                </div>

                {/* Caractéristiques */}
                <div className="grid grid-cols-2 gap-4 mt-4">
                    <div className="flex items-center text-sm text-gray-600">
                        <CalendarIcon className="h-4 w-4 mr-2" />
                        <span>{vehicle.year}</span>
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                        <SpeedometerIcon className="h-4 w-4 mr-2" />
                        <span>{vehicle.mileage} km</span>
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                        <FuelIcon className="h-4 w-4 mr-2" />
                        <span>{vehicle.fuel_type}</span>
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                        <ShieldCheckIcon className="h-4 w-4 mr-2" />
                        <span>{vehicle.safety_rating}/5</span>
                    </div>
                </div>

                {/* Prix et bouton d'action */}
                <div className="mt-4 flex justify-between items-center">
                    <div>
                        <p className="text-2xl font-bold text-blue-600">
                            {new Intl.NumberFormat('fr-FR', {
                                style: 'currency',
                                currency: 'EUR'
                            }).format(vehicle.price)}
                        </p>
                        {vehicle.price_rating && (
                            <span className={`text-xs font-medium ${
                                vehicle.price_rating === 'Bon prix' ? 'text-green-600' : 
                                vehicle.price_rating === 'Prix élevé' ? 'text-orange-600' : 
                                'text-gray-600'
                            }`}>
                                {vehicle.price_rating}
                            </span>
                        )}
                    </div>
                    <button
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                        onClick={(e) => {
                            e.stopPropagation();
                            // Action spécifique (par exemple, sauvegarder)
                        }}
                    >
                        Détails
                    </button>
                </div>
            </div>
        </motion.div>
    );
};

export default VehicleCard;
