import React from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { ClockIcon, TrashIcon } from '@heroicons/react/outline';
import { getSavedSearches, deleteSavedSearch } from '../../api/search';
import { useToast } from '../../hooks/useToast';

const SavedSearches = ({ onSelect }) => {
    const queryClient = useQueryClient();
    const { showToast } = useToast();
    
    const { data: searches, isLoading } = useQuery(
        'saved-searches',
        getSavedSearches
    );
    
    const deleteMutation = useMutation(deleteSavedSearch, {
        onSuccess: () => {
            queryClient.invalidateQueries('saved-searches');
            showToast('Recherche supprimée', 'success');
        },
        onError: () => {
            showToast(
                'Erreur lors de la suppression de la recherche',
                'error'
            );
        }
    });
    
    if (isLoading || !searches?.length) {
        return null;
    }
    
    return (
        <div className="bg-white rounded-lg shadow-sm p-4">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Recherches sauvegardées
            </h2>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {searches.map((search) => (
                    <div
                        key={search.id}
                        className="relative group border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors duration-200"
                    >
                        <div
                            onClick={() => onSelect(search.params)}
                            className="cursor-pointer"
                        >
                            <div className="flex items-center space-x-2 text-sm text-gray-600 mb-2">
                                <ClockIcon className="w-4 h-4" />
                                <span>
                                    {new Date(search.created_at).toLocaleDateString()}
                                </span>
                            </div>
                            
                            <h3 className="font-medium text-gray-900 mb-1">
                                {search.name}
                            </h3>
                            
                            <div className="text-sm text-gray-600">
                                {search.params.make && search.params.model ? (
                                    <span>
                                        {search.params.make} {search.params.model}
                                    </span>
                                ) : (
                                    <span>Tous les véhicules</span>
                                )}
                                {search.params.location && (
                                    <span className="ml-2">
                                        • {search.params.location}
                                    </span>
                                )}
                            </div>
                        </div>
                        
                        {/* Bouton de suppression */}
                        <button
                            onClick={() => deleteMutation.mutate(search.id)}
                            className="absolute top-2 right-2 p-1 text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                            title="Supprimer cette recherche"
                        >
                            <TrashIcon className="w-4 h-4" />
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SavedSearches;
