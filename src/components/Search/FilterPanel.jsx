import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    AdjustmentsIcon,
    XIcon,
    ChevronDownIcon
} from '@heroicons/react/outline';
import RangeSlider from '../common/RangeSlider';

const FilterSection = ({ title, children, defaultOpen = false }) => {
    const [isOpen, setIsOpen] = useState(defaultOpen);

    return (
        <div className="border-b border-gray-200 py-4">
            <button
                className="w-full flex justify-between items-center text-left"
                onClick={() => setIsOpen(!isOpen)}
            >
                <span className="text-sm font-medium text-gray-700">{title}</span>
                <ChevronDownIcon
                    className={`h-5 w-5 text-gray-400 transform transition-transform ${
                        isOpen ? 'rotate-180' : ''
                    }`}
                />
            </button>
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        className="overflow-hidden"
                    >
                        <div className="pt-4">{children}</div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

const FilterPanel = ({ filters, onChange, onReset }) => {
    const [showMobileFilters, setShowMobileFilters] = useState(false);

    const filterContent = (
        <div className="space-y-2">
            {/* Prix */}
            <FilterSection title="Prix" defaultOpen={true}>
                <RangeSlider
                    min={0}
                    max={100000}
                    step={1000}
                    value={filters.price}
                    onChange={(value) => onChange({ ...filters, price: value })}
                    formatLabel={(value) => `${value.toLocaleString()}€`}
                />
            </FilterSection>

            {/* Année */}
            <FilterSection title="Année">
                <RangeSlider
                    min={2000}
                    max={new Date().getFullYear()}
                    step={1}
                    value={filters.year}
                    onChange={(value) => onChange({ ...filters, year: value })}
                />
            </FilterSection>

            {/* Kilométrage */}
            <FilterSection title="Kilométrage">
                <RangeSlider
                    min={0}
                    max={300000}
                    step={5000}
                    value={filters.mileage}
                    onChange={(value) => onChange({ ...filters, mileage: value })}
                    formatLabel={(value) => `${value.toLocaleString()} km`}
                />
            </FilterSection>

            {/* Carburant */}
            <FilterSection title="Carburant">
                <div className="space-y-2">
                    {['Essence', 'Diesel', 'Électrique', 'Hybride'].map((fuel) => (
                        <label key={fuel} className="flex items-center">
                            <input
                                type="checkbox"
                                className="form-checkbox h-4 w-4 text-blue-600"
                                checked={filters.fuel_types?.includes(fuel)}
                                onChange={(e) => {
                                    const newFuelTypes = e.target.checked
                                        ? [...(filters.fuel_types || []), fuel]
                                        : (filters.fuel_types || []).filter(
                                              (f) => f !== fuel
                                          );
                                    onChange({
                                        ...filters,
                                        fuel_types: newFuelTypes,
                                    });
                                }}
                            />
                            <span className="ml-2 text-sm text-gray-700">
                                {fuel}
                            </span>
                        </label>
                    ))}
                </div>
            </FilterSection>

            {/* Note de sécurité */}
            <FilterSection title="Sécurité">
                <div className="space-y-2">
                    {[5, 4, 3, 2, 1].map((rating) => (
                        <label key={rating} className="flex items-center">
                            <input
                                type="checkbox"
                                className="form-checkbox h-4 w-4 text-blue-600"
                                checked={filters.safety_ratings?.includes(rating)}
                                onChange={(e) => {
                                    const newRatings = e.target.checked
                                        ? [...(filters.safety_ratings || []), rating]
                                        : (filters.safety_ratings || []).filter(
                                              (r) => r !== rating
                                          );
                                    onChange({
                                        ...filters,
                                        safety_ratings: newRatings,
                                    });
                                }}
                            />
                            <span className="ml-2 text-sm text-gray-700">
                                {rating} étoiles et plus
                            </span>
                        </label>
                    ))}
                </div>
            </FilterSection>

            {/* Bouton de réinitialisation */}
            <div className="pt-4">
                <button
                    onClick={onReset}
                    className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-4 rounded-md text-sm font-medium transition-colors"
                >
                    Réinitialiser les filtres
                </button>
            </div>
        </div>
    );

    return (
        <>
            {/* Version desktop */}
            <div className="hidden md:block w-64 flex-shrink-0">
                {filterContent}
            </div>

            {/* Version mobile */}
            <div className="md:hidden">
                <button
                    className="flex items-center text-sm font-medium text-gray-700"
                    onClick={() => setShowMobileFilters(true)}
                >
                    <AdjustmentsIcon className="h-5 w-5 mr-2" />
                    Filtres
                </button>

                <AnimatePresence>
                    {showMobileFilters && (
                        <>
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 0.5 }}
                                exit={{ opacity: 0 }}
                                className="fixed inset-0 bg-black"
                                onClick={() => setShowMobileFilters(false)}
                            />
                            <motion.div
                                initial={{ x: '100%' }}
                                animate={{ x: 0 }}
                                exit={{ x: '100%' }}
                                className="fixed inset-y-0 right-0 w-full max-w-xs bg-white shadow-xl p-6 overflow-y-auto"
                            >
                                <div className="flex justify-between items-center mb-6">
                                    <h2 className="text-lg font-medium text-gray-900">
                                        Filtres
                                    </h2>
                                    <button
                                        className="text-gray-400 hover:text-gray-500"
                                        onClick={() => setShowMobileFilters(false)}
                                    >
                                        <XIcon className="h-6 w-6" />
                                    </button>
                                </div>
                                {filterContent}
                            </motion.div>
                        </>
                    )}
                </AnimatePresence>
            </div>
        </>
    );
};

export default FilterPanel;
