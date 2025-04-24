import React from 'react';
import { motion } from 'framer-motion';
import {
    CheckCircleIcon,
    ExclamationIcon,
    ClockIcon,
    DocumentTextIcon,
    CogIcon,
    LocationMarkerIcon
} from '@heroicons/react/outline';

const TimelineEvent = ({ date, title, description, type, details }) => {
    const getEventStyle = () => {
        switch (type) {
            case 'maintenance':
                return {
                    icon: CogIcon,
                    color: 'text-blue-500',
                    bg: 'bg-blue-100'
                };
            case 'accident':
                return {
                    icon: ExclamationIcon,
                    color: 'text-red-500',
                    bg: 'bg-red-100'
                };
            case 'ownership':
                return {
                    icon: DocumentTextIcon,
                    color: 'text-purple-500',
                    bg: 'bg-purple-100'
                };
            case 'inspection':
                return {
                    icon: CheckCircleIcon,
                    color: 'text-green-500',
                    bg: 'bg-green-100'
                };
            default:
                return {
                    icon: ClockIcon,
                    color: 'text-gray-500',
                    bg: 'bg-gray-100'
                };
        }
    };

    const { icon: Icon, color, bg } = getEventStyle();

    return (
        <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex gap-4"
        >
            <div className="flex flex-col items-center">
                <div className={`w-10 h-10 rounded-full ${bg} flex items-center justify-center`}>
                    <Icon className={`w-5 h-5 ${color}`} />
                </div>
                <div className="flex-1 w-px bg-gray-200" />
            </div>
            <div className="flex-1 pb-8">
                <div className="bg-white rounded-lg shadow-sm p-4">
                    <div className="flex justify-between items-start mb-2">
                        <div>
                            <h3 className="text-lg font-medium text-gray-900">
                                {title}
                            </h3>
                            <p className="text-sm text-gray-500">
                                {new Date(date).toLocaleDateString('fr-FR', {
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric'
                                })}
                            </p>
                        </div>
                        <div className={`px-2 py-1 rounded-full text-sm ${bg} ${color}`}>
                            {type}
                        </div>
                    </div>
                    <p className="text-gray-600 mb-4">{description}</p>
                    {details && (
                        <div className="border-t pt-4 mt-4">
                            <dl className="grid grid-cols-1 gap-x-4 gap-y-4 sm:grid-cols-2">
                                {Object.entries(details).map(([key, value]) => (
                                    <div key={key} className="sm:col-span-1">
                                        <dt className="text-sm font-medium text-gray-500">
                                            {key}
                                        </dt>
                                        <dd className="mt-1 text-sm text-gray-900">
                                            {value}
                                        </dd>
                                    </div>
                                ))}
                            </dl>
                        </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
};

const VehicleHistory = ({ history }) => {
    return (
        <div className="max-w-3xl mx-auto">
            <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                    Résumé de l'historique
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-green-50 rounded-lg p-4">
                        <div className="flex items-center mb-2">
                            <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2" />
                            <span className="font-medium text-green-700">
                                Points positifs
                            </span>
                        </div>
                        <ul className="text-sm text-green-600 space-y-1">
                            <li>• Entretien régulier</li>
                            <li>• Aucun accident majeur</li>
                            <li>• Kilométrage certifié</li>
                        </ul>
                    </div>
                    <div className="bg-yellow-50 rounded-lg p-4">
                        <div className="flex items-center mb-2">
                            <ExclamationIcon className="h-5 w-5 text-yellow-500 mr-2" />
                            <span className="font-medium text-yellow-700">
                                Points d'attention
                            </span>
                        </div>
                        <ul className="text-sm text-yellow-600 space-y-1">
                            <li>• Changement de propriétaire fréquent</li>
                            <li>• Quelques réparations mineures</li>
                        </ul>
                    </div>
                    <div className="bg-blue-50 rounded-lg p-4">
                        <div className="flex items-center mb-2">
                            <DocumentTextIcon className="h-5 w-5 text-blue-500 mr-2" />
                            <span className="font-medium text-blue-700">
                                Documents
                            </span>
                        </div>
                        <ul className="text-sm text-blue-600 space-y-1">
                            <li>• Carnet d'entretien complet</li>
                            <li>• Factures disponibles</li>
                            <li>• Certificats de contrôle</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div className="space-y-6">
                {history.map((event, index) => (
                    <TimelineEvent
                        key={index}
                        date={event.date}
                        title={event.title}
                        description={event.description}
                        type={event.type}
                        details={event.details}
                    />
                ))}
            </div>
        </div>
    );
};

export default VehicleHistory;
