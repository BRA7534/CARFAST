import React, { useState } from 'react';
import { useInfiniteQuery } from 'react-query';
import { useInView } from 'react-intersection-observer';
import { motion, AnimatePresence } from 'framer-motion';
import { searchVehicles } from '../../api/search';
import VehicleCard from './VehicleCard';
import FilterPanel from './FilterPanel';
import Loader from '../common/Loader';
import VehicleModal from './VehicleModal';

const SearchResults = ({ searchParams }) => {
    const { ref, inView } = useInView();
    const [selectedVehicle, setSelectedVehicle] = useState(null);
    const [filters, setFilters] = useState({
        price: [0, 100000],
        year: [2000, new Date().getFullYear()],
        mileage: [0, 300000],
        fuel_types: [],
        safety_ratings: []
    });
    
    const {
        data,
        isLoading,
        isError,
        error,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage
    } = useInfiniteQuery(
        ['vehicles', searchParams, filters],
        ({ pageParam = 1 }) => searchVehicles({ 
            ...searchParams, 
            ...filters,
            page: pageParam 
        }),
        {
            getNextPageParam: (lastPage) => 
                lastPage.page < lastPage.pages ? lastPage.page + 1 : undefined,
        }
    );
    
    // Charger plus de résultats quand on atteint le bas
    React.useEffect(() => {
        if (inView && hasNextPage) {
            fetchNextPage();
        }
    }, [inView, fetchNextPage, hasNextPage]);

    const handleVehicleClick = (vehicle) => {
        setSelectedVehicle(vehicle);
    };

    const handleCloseModal = () => {
        setSelectedVehicle(null);
    };
    
    if (isLoading) {
        return <Loader />;
    }
    
    if (isError) {
        return (
            <div className="text-center py-12">
                <p className="text-red-600">
                    {error.response?.data?.subscription_required
                        ? "Abonnement requis pour voir les résultats"
                        : "Erreur lors du chargement des résultats"}
                </p>
            </div>
        );
    }

    return (
        <div className="flex gap-6">
            {/* Panneau de filtres */}
            <FilterPanel
                filters={filters}
                onChange={setFilters}
                onReset={() => setFilters({
                    price: [0, 100000],
                    year: [2000, new Date().getFullYear()],
                    mileage: [0, 300000],
                    fuel_types: [],
                    safety_ratings: []
                })}
            />

            {/* Liste des véhicules */}
            <div className="flex-1">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <AnimatePresence>
                        {data?.pages.map((page) =>
                            page.vehicles.map((vehicle) => (
                                <VehicleCard
                                    key={vehicle.id}
                                    vehicle={vehicle}
                                    onClick={handleVehicleClick}
                                />
                            ))
                        )}
                    </AnimatePresence>
                </div>

                {/* Loader pour le chargement infini */}
                {(isFetchingNextPage || hasNextPage) && (
                    <div ref={ref} className="flex justify-center py-8">
                        <Loader />
                    </div>
                )}
            </div>

            {/* Modal de détails du véhicule */}
            <AnimatePresence>
                {selectedVehicle && (
                    <VehicleModal
                        vehicle={selectedVehicle}
                        onClose={handleCloseModal}
                    />
                )}
            </AnimatePresence>
        </div>
    );
};

export default SearchResults;
