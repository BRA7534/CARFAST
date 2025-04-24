import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useQuery, useMutation } from 'react-query';
import { SearchIcon, FilterIcon, SaveIcon } from '@heroicons/react/outline';
import Select from 'react-select';
import RangeSlider from '../common/RangeSlider';
import { searchVehicles, getFilters, saveSearch } from '../../api/search';
import { useAuth } from '../../hooks/useAuth';
import { useToast } from '../../hooks/useToast';

const SearchForm = ({ onSearch }) => {
    const { register, handleSubmit, watch, setValue, reset } = useForm();
    const { user } = useAuth();
    const { showToast } = useToast();
    const [showFilters, setShowFilters] = useState(false);
    const [locationSuggestions, setLocationSuggestions] = useState([]);
    
    // Récupérer les filtres
    const { data: filters } = useQuery('filters', getFilters);
    
    // Observer les changements de marque pour mettre à jour les modèles
    const selectedMake = watch('make');
    
    useEffect(() => {
        if (selectedMake) {
            // Mettre à jour les modèles disponibles
            setValue('model', '');
        }
    }, [selectedMake]);
    
    // Mutation pour sauvegarder la recherche
    const saveMutation = useMutation(saveSearch, {
        onSuccess: () => {
            showToast('Recherche sauvegardée avec succès', 'success');
        },
        onError: (error) => {
            if (error.response?.data?.upgrade_required) {
                showToast(
                    'Limite de recherches atteinte. Mettez à niveau votre abonnement.',
                    'warning'
                );
            } else {
                showToast(
                    'Erreur lors de la sauvegarde de la recherche',
                    'error'
                );
            }
        }
    });
    
    const onSubmit = async (data) => {
        try {
            const results = await searchVehicles(data);
            onSearch(results);
        } catch (error) {
            if (error.response?.data?.subscription_required) {
                showToast(
                    'Abonnement requis pour effectuer des recherches',
                    'warning'
                );
            } else {
                showToast(
                    'Erreur lors de la recherche',
                    'error'
                );
            }
        }
    };
    
    const handleSaveSearch = () => {
        const searchParams = watch();
        saveMutation.mutate({
            params: searchParams,
            name: 'Ma recherche'  // À personnaliser
        });
    };
    
    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Barre de recherche principale */}
            <div className="flex space-x-4">
                <div className="flex-1">
                    <input
                        type="text"
                        placeholder="Rechercher une voiture..."
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        {...register('query')}
                    />
                </div>
                <button
                    type="submit"
                    className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                    <SearchIcon className="w-5 h-5" />
                </button>
                <button
                    type="button"
                    onClick={() => setShowFilters(!showFilters)}
                    className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                    <FilterIcon className="w-5 h-5 text-gray-600" />
                </button>
                {user && (
                    <button
                        type="button"
                        onClick={handleSaveSearch}
                        className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    >
                        <SaveIcon className="w-5 h-5 text-gray-600" />
                    </button>
                )}
            </div>
            
            {/* Filtres avancés */}
            {showFilters && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6 bg-white rounded-lg shadow">
                    {/* Marque */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Marque
                        </label>
                        <Select
                            options={filters?.makes.map(make => ({
                                value: make,
                                label: make
                            }))}
                            onChange={(option) => setValue('make', option.value)}
                            isClearable
                            placeholder="Toutes les marques"
                            className="basic-select"
                            classNamePrefix="select"
                        />
                    </div>
                    
                    {/* Modèle */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Modèle
                        </label>
                        <Select
                            options={filters?.models.map(model => ({
                                value: model,
                                label: model
                            }))}
                            onChange={(option) => setValue('model', option.value)}
                            isDisabled={!selectedMake}
                            isClearable
                            placeholder="Tous les modèles"
                            className="basic-select"
                            classNamePrefix="select"
                        />
                    </div>
                    
                    {/* Année */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Année
                        </label>
                        <div className="flex space-x-4">
                            <Select
                                options={filters?.years.map(year => ({
                                    value: year,
                                    label: year
                                }))}
                                onChange={(option) => setValue('year_min', option.value)}
                                isClearable
                                placeholder="Min"
                                className="w-1/2"
                            />
                            <Select
                                options={filters?.years.map(year => ({
                                    value: year,
                                    label: year
                                }))}
                                onChange={(option) => setValue('year_max', option.value)}
                                isClearable
                                placeholder="Max"
                                className="w-1/2"
                            />
                        </div>
                    </div>
                    
                    {/* Prix */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Prix
                        </label>
                        <RangeSlider
                            min={0}
                            max={200000}
                            step={1000}
                            onChange={([min, max]) => {
                                setValue('price_min', min);
                                setValue('price_max', max);
                            }}
                        />
                    </div>
                    
                    {/* Kilométrage */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Kilométrage
                        </label>
                        <RangeSlider
                            min={0}
                            max={300000}
                            step={5000}
                            onChange={([min, max]) => {
                                setValue('mileage_min', min);
                                setValue('mileage_max', max);
                            }}
                        />
                    </div>
                    
                    {/* Carburant */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Carburant
                        </label>
                        <Select
                            options={filters?.fuel_types.map(type => ({
                                value: type,
                                label: type
                            }))}
                            onChange={(option) => setValue('fuel_type', option.value)}
                            isClearable
                            placeholder="Tous les carburants"
                            className="basic-select"
                            classNamePrefix="select"
                        />
                    </div>
                    
                    {/* Transmission */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Transmission
                        </label>
                        <Select
                            options={filters?.transmissions.map(trans => ({
                                value: trans,
                                label: trans
                            }))}
                            onChange={(option) => setValue('transmission', option.value)}
                            isClearable
                            placeholder="Toutes les transmissions"
                            className="basic-select"
                            classNamePrefix="select"
                        />
                    </div>
                    
                    {/* Localisation */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Localisation
                        </label>
                        <div className="flex space-x-4">
                            <input
                                type="text"
                                placeholder="Ville ou code postal"
                                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                {...register('location')}
                            />
                            <Select
                                options={[
                                    { value: 10, label: '10 km' },
                                    { value: 25, label: '25 km' },
                                    { value: 50, label: '50 km' },
                                    { value: 100, label: '100 km' },
                                    { value: 200, label: '200 km' }
                                ]}
                                onChange={(option) => setValue('radius', option.value)}
                                placeholder="Rayon"
                                className="w-32"
                            />
                        </div>
                    </div>
                    
                    {/* Tri */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Trier par
                        </label>
                        <Select
                            options={filters?.sort_options}
                            onChange={(option) => setValue('sort_by', option.value)}
                            defaultValue={filters?.sort_options[0]}
                            className="basic-select"
                            classNamePrefix="select"
                        />
                    </div>
                    
                    {/* Boutons */}
                    <div className="col-span-full flex justify-end space-x-4">
                        <button
                            type="button"
                            onClick={() => reset()}
                            className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
                        >
                            Réinitialiser
                        </button>
                        <button
                            type="submit"
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                        >
                            Rechercher
                        </button>
                    </div>
                </div>
            )}
        </form>
    );
};

export default SearchForm;
