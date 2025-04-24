import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
    SearchIcon, 
    ShieldCheckIcon, 
    DocumentSearchIcon,
    ChartBarIcon,
    CheckCircleIcon 
} from '@heroicons/react/outline';
import HistoVecIntegration from '../components/Vehicle/HistoVecIntegration';

const FeatureCard = ({ icon: Icon, title, description }) => (
    <motion.div
        whileHover={{ y: -5 }}
        className="bg-white p-6 rounded-xl shadow-lg"
    >
        <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <Icon className="h-6 w-6 text-blue-600" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
        <p className="text-gray-600">{description}</p>
    </motion.div>
);

const Home = () => {
    const [vehicleData, setVehicleData] = useState(null);

    const handleVehicleDataReceived = (data) => {
        setVehicleData(data);
        document.getElementById('vehicle-results')?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleScrollToSection = (sectionId) => {
        document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' });
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
            {/* Hero Section */}
            <div className="relative overflow-hidden">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="text-center"
                    >
                        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                            Vérifiez l'historique de votre futur véhicule
                        </h1>
                        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                            CarFast vous permet d'accéder à l'historique complet, aux informations 
                            techniques et aux rapports de sécurité de plus de 10 millions de véhicules.
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <button
                                onClick={() => handleScrollToSection('vehicle-search')}
                                className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                            >
                                <SearchIcon className="h-5 w-5 mr-2" />
                                Vérifier un véhicule
                            </button>
                            <button
                                onClick={() => handleScrollToSection('how-it-works')}
                                className="inline-flex items-center px-8 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                            >
                                En savoir plus
                            </button>
                        </div>
                    </motion.div>
                </div>

                {/* Formes décoratives */}
                <div className="absolute top-0 inset-x-0 flex justify-center overflow-hidden pointer-events-none">
                    <div className="w-[108rem] flex-none flex justify-end">
                        <motion.img
                            src="/images/hero-background.svg"
                            alt=""
                            className="w-[71.75rem] flex-none max-w-none"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 0.1 }}
                            transition={{ duration: 1 }}
                        />
                    </div>
                </div>
            </div>

            {/* Section Recherche HistoVec */}
            <div className="py-16 bg-gray-50" id="vehicle-search">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-12">
                        <h2 className="text-3xl font-bold text-gray-900 mb-4">
                            Vérifiez votre véhicule avec HistoVec
                        </h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Accédez aux données officielles du Ministère de l'Intérieur pour vérifier 
                            l'historique complet de votre véhicule.
                        </p>
                    </div>

                    <div className="max-w-3xl mx-auto">
                        <HistoVecIntegration onVehicleDataReceived={handleVehicleDataReceived} />
                    </div>
                </div>
            </div>

            {/* Section Résultats */}
            {vehicleData && (
                <div className="py-16 bg-white" id="vehicle-results">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="space-y-8">
                            {/* Message de succès */}
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="bg-green-50 border border-green-100 rounded-lg p-4 flex items-center"
                            >
                                <CheckCircleIcon className="h-6 w-6 text-green-500 mr-3" />
                                <span className="text-green-800">
                                    Les informations du véhicule ont été récupérées avec succès !
                                </span>
                            </motion.div>

                            {/* Informations du véhicule */}
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.2 }}
                                className="bg-white rounded-lg shadow-sm p-6"
                            >
                                <h3 className="text-lg font-medium text-gray-900 mb-6">
                                    Informations du véhicule
                                </h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    <div>
                                        <h4 className="text-sm font-medium text-gray-500">Marque</h4>
                                        <p className="mt-1 text-lg text-gray-900">{vehicleData.marque}</p>
                                    </div>
                                    <div>
                                        <h4 className="text-sm font-medium text-gray-500">Modèle</h4>
                                        <p className="mt-1 text-lg text-gray-900">{vehicleData.modele}</p>
                                    </div>
                                    <div>
                                        <h4 className="text-sm font-medium text-gray-500">Version</h4>
                                        <p className="mt-1 text-lg text-gray-900">{vehicleData.version || "Non spécifié"}</p>
                                    </div>
                                    <div>
                                        <h4 className="text-sm font-medium text-gray-500">Mise en circulation</h4>
                                        <p className="mt-1 text-lg text-gray-900">{vehicleData.datePremiereMiseEnCirculation}</p>
                                    </div>
                                    <div>
                                        <h4 className="text-sm font-medium text-gray-500">Puissance fiscale</h4>
                                        <p className="mt-1 text-lg text-gray-900">{vehicleData.puissanceFiscale} CV</p>
                                    </div>
                                    <div>
                                        <h4 className="text-sm font-medium text-gray-500">Énergie</h4>
                                        <p className="mt-1 text-lg text-gray-900">{vehicleData.energie}</p>
                                    </div>
                                </div>
                            </motion.div>

                            {/* État administratif */}
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.4 }}
                                className="bg-white rounded-lg shadow-sm p-6"
                            >
                                <h3 className="text-lg font-medium text-gray-900 mb-6">
                                    État administratif
                                </h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className={`rounded-lg p-4 ${
                                        vehicleData.situation?.isGage 
                                            ? 'bg-red-50 text-red-800' 
                                            : 'bg-green-50 text-green-800'
                                    }`}>
                                        <h4 className="font-medium mb-1">Situation du gage</h4>
                                        <p>{vehicleData.situation?.isGage ? 'Véhicule gagé' : 'Véhicule non gagé'}</p>
                                    </div>
                                    <div className={`rounded-lg p-4 ${
                                        vehicleData.situation?.isVole 
                                            ? 'bg-red-50 text-red-800' 
                                            : 'bg-green-50 text-green-800'
                                    }`}>
                                        <h4 className="font-medium mb-1">Situation du vol</h4>
                                        <p>{vehicleData.situation?.isVole ? 'Véhicule déclaré volé' : 'Véhicule non volé'}</p>
                                    </div>
                                    <div className={`rounded-lg p-4 ${
                                        vehicleData.situation?.isPerteTotale 
                                            ? 'bg-red-50 text-red-800' 
                                            : 'bg-green-50 text-green-800'
                                    }`}>
                                        <h4 className="font-medium mb-1">Perte totale</h4>
                                        <p>{vehicleData.situation?.isPerteTotale ? 'Véhicule déclaré en perte totale' : 'Aucune perte totale déclarée'}</p>
                                    </div>
                                    <div className="rounded-lg p-4 bg-blue-50 text-blue-800">
                                        <h4 className="font-medium mb-1">Dernier changement</h4>
                                        <p>{vehicleData.situation?.dateDernierChangementTitulaire || "Pas de changement récent"}</p>
                                    </div>
                                </div>
                            </motion.div>

                            {/* Historique */}
                            {vehicleData.historique && vehicleData.historique.length > 0 && (
                                <motion.div
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.6 }}
                                    className="bg-white rounded-lg shadow-sm p-6"
                                >
                                    <h3 className="text-lg font-medium text-gray-900 mb-6">
                                        Historique du véhicule
                                    </h3>
                                    <div className="space-y-4">
                                        {vehicleData.historique.map((event, index) => (
                                            <div 
                                                key={index}
                                                className="flex items-start space-x-4 p-4 border-l-4 border-blue-500"
                                            >
                                                <div className="min-w-[100px] text-sm text-gray-500">
                                                    {event.date}
                                                </div>
                                                <div>
                                                    <h4 className="font-medium text-gray-900">
                                                        {event.type}
                                                    </h4>
                                                    <p className="text-gray-600 mt-1">
                                                        {event.description}
                                                    </p>
                                                    {event.lieu && (
                                                        <p className="text-sm text-gray-500 mt-1">
                                                            Lieu : {event.lieu}
                                                        </p>
                                                    )}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </motion.div>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Section Caractéristiques */}
            <div className="py-24 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl font-bold text-gray-900 mb-4">
                            Pourquoi choisir CarFast ?
                        </h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Notre plateforme vous offre tous les outils nécessaires pour faire 
                            un choix éclairé lors de l'achat de votre prochain véhicule.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        <FeatureCard
                            icon={DocumentSearchIcon}
                            title="Historique complet"
                            description="Accédez à l'historique détaillé du véhicule : propriétaires, entretiens, accidents, et plus encore."
                        />
                        <FeatureCard
                            icon={ShieldCheckIcon}
                            title="Vérification de sécurité"
                            description="Consultez les rapports de sécurité, les rappels constructeur et les notes des crash-tests."
                        />
                        <FeatureCard
                            icon={ChartBarIcon}
                            title="Analyse du marché"
                            description="Comparez les prix du marché et recevez une estimation précise de la valeur du véhicule."
                        />
                    </div>
                </div>
            </div>

            {/* Section Comment ça marche */}
            <div id="how-it-works" className="py-24 bg-gray-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl font-bold text-gray-900 mb-4">
                            Comment ça marche ?
                        </h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            En quelques étapes simples, obtenez toutes les informations 
                            dont vous avez besoin sur votre futur véhicule.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {[
                            {
                                step: '01',
                                title: 'Recherchez',
                                description: 'Entrez le numéro d'immatriculation ou les caractéristiques du véhicule'
                            },
                            {
                                step: '02',
                                title: 'Analysez',
                                description: 'Consultez l'historique complet et les rapports détaillés'
                            },
                            {
                                step: '03',
                                title: 'Décidez',
                                description: 'Prenez une décision éclairée basée sur des données fiables'
                            }
                        ].map((item) => (
                            <motion.div
                                key={item.step}
                                whileHover={{ scale: 1.05 }}
                                className="relative bg-white p-8 rounded-xl shadow-lg"
                            >
                                <div className="absolute -top-4 -left-4 w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                                    {item.step}
                                </div>
                                <h3 className="text-xl font-semibold text-gray-900 mb-4 mt-4">
                                    {item.title}
                                </h3>
                                <p className="text-gray-600">{item.description}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Section CTA */}
            <div className="bg-blue-600">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                    <div className="text-center">
                        <h2 className="text-3xl font-bold text-white mb-4">
                            Prêt à vérifier votre prochain véhicule ?
                        </h2>
                        <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
                            Rejoignez les milliers d'utilisateurs qui font confiance à CarFast 
                            pour leur achat automobile.
                        </p>
                        <Link
                            to="/register"
                            className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-blue-50"
                        >
                            Commencer gratuitement
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;
