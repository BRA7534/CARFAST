import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { XIcon, PlusIcon } from '@heroicons/react/outline';

const CompareTable = ({ vehicles, onRemove, onAdd }) => {
    const categories = [
        {
            name: 'Informations générales',
            fields: [
                { key: 'make', label: 'Marque' },
                { key: 'model', label: 'Modèle' },
                { key: 'year', label: 'Année' },
                { key: 'price', label: 'Prix', format: (value) => 
                    new Intl.NumberFormat('fr-FR', {
                        style: 'currency',
                        currency: 'EUR'
                    }).format(value)
                }
            ]
        },
        {
            name: 'Caractéristiques',
            fields: [
                { key: 'mileage', label: 'Kilométrage', format: (value) => 
                    `${value.toLocaleString()} km`
                },
                { key: 'fuel_type', label: 'Carburant' },
                { key: 'transmission', label: 'Transmission' },
                { key: 'engine_size', label: 'Moteur' }
            ]
        },
        {
            name: 'Performance',
            fields: [
                { key: 'power', label: 'Puissance' },
                { key: 'acceleration', label: '0-100 km/h' },
                { key: 'top_speed', label: 'Vitesse max' },
                { key: 'fuel_consumption', label: 'Consommation' }
            ]
        },
        {
            name: 'Sécurité',
            fields: [
                { key: 'safety_rating', label: 'Note globale' },
                { key: 'airbags', label: 'Airbags' },
                { key: 'assistance_systems', label: 'Systèmes d\'assistance' },
                { key: 'crash_test', label: 'Crash test' }
            ]
        }
    ];

    const maxVehicles = 3;

    return (
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            {/* En-têtes des véhicules */}
            <div className="grid grid-cols-[200px_repeat(3,1fr)] border-b">
                <div className="p-4 font-medium text-gray-700 bg-gray-50">
                    Comparaison
                </div>
                {Array.from({ length: maxVehicles }).map((_, index) => (
                    <div key={index} className="p-4 relative">
                        <AnimatePresence>
                            {vehicles[index] ? (
                                <motion.div
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -20 }}
                                    className="relative"
                                >
                                    <img
                                        src={vehicles[index].image_url || '/placeholder-car.jpg'}
                                        alt={`${vehicles[index].make} ${vehicles[index].model}`}
                                        className="w-full h-48 object-cover rounded-lg"
                                    />
                                    <button
                                        onClick={() => onRemove(index)}
                                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
                                    >
                                        <XIcon className="h-4 w-4" />
                                    </button>
                                    <h3 className="mt-2 font-medium text-gray-900">
                                        {vehicles[index].make} {vehicles[index].model}
                                    </h3>
                                    <p className="text-sm text-gray-500">
                                        {vehicles[index].year}
                                    </p>
                                </motion.div>
                            ) : (
                                <motion.button
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    exit={{ opacity: 0 }}
                                    onClick={onAdd}
                                    className="w-full h-48 border-2 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center text-gray-500 hover:text-gray-700 hover:border-gray-400"
                                >
                                    <PlusIcon className="h-8 w-8 mb-2" />
                                    <span>Ajouter un véhicule</span>
                                </motion.button>
                            )}
                        </AnimatePresence>
                    </div>
                ))}
            </div>

            {/* Tableau de comparaison */}
            {categories.map((category) => (
                <div key={category.name}>
                    {/* En-tête de catégorie */}
                    <div className="grid grid-cols-[200px_repeat(3,1fr)] bg-gray-50">
                        <div className="p-4 font-medium text-gray-900">
                            {category.name}
                        </div>
                        <div className="col-span-3" />
                    </div>

                    {/* Champs de la catégorie */}
                    {category.fields.map((field) => (
                        <div
                            key={field.key}
                            className="grid grid-cols-[200px_repeat(3,1fr)] border-t"
                        >
                            <div className="p-4 text-sm text-gray-600 bg-gray-50">
                                {field.label}
                            </div>
                            {Array.from({ length: maxVehicles }).map((_, index) => (
                                <div
                                    key={index}
                                    className="p-4 text-sm text-gray-900"
                                >
                                    {vehicles[index] && (
                                        <motion.div
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            className={
                                                getBestValueClass(
                                                    vehicles,
                                                    field.key,
                                                    vehicles[index][field.key]
                                                )
                                            }
                                        >
                                            {field.format
                                                ? field.format(vehicles[index][field.key])
                                                : vehicles[index][field.key]}
                                        </motion.div>
                                    )}
                                </div>
                            ))}
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};

// Fonction utilitaire pour mettre en évidence les meilleures valeurs
const getBestValueClass = (vehicles, key, value) => {
    if (!vehicles || !key || value === undefined) return '';

    const numericFields = [
        'price',
        'mileage',
        'acceleration',
        'fuel_consumption',
        'safety_rating'
    ];

    if (!numericFields.includes(key)) return '';

    const values = vehicles
        .filter(Boolean)
        .map((v) => v[key])
        .filter((v) => v !== undefined);

    if (values.length < 2) return '';

    const isLowestBetter = ['price', 'mileage', 'acceleration', 'fuel_consumption'];
    const isHighestBetter = ['safety_rating', 'power', 'top_speed'];

    if (isLowestBetter.includes(key)) {
        if (value === Math.min(...values)) {
            return 'text-green-600 font-medium';
        }
    } else if (isHighestBetter.includes(key)) {
        if (value === Math.max(...values)) {
            return 'text-green-600 font-medium';
        }
    }

    return '';
};

export default CompareTable;
