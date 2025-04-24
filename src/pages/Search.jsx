import React, { useState } from 'react';
import { Helmet } from 'react-helmet';
import SearchForm from '../components/Search/SearchForm';
import SearchResults from '../components/Search/SearchResults';
import SavedSearches from '../components/Search/SavedSearches';
import { useAuth } from '../hooks/useAuth';

const Search = () => {
    const { user } = useAuth();
    const [searchParams, setSearchParams] = useState(null);
    
    const handleSearch = (params) => {
        setSearchParams(params);
        // Sauvegarder dans l'historique pour le retour arrière
        window.history.pushState(
            { searchParams: params },
            '',
            `/search?${new URLSearchParams(params).toString()}`
        );
    };
    
    return (
        <>
            <Helmet>
                <title>Rechercher un véhicule | CarFast</title>
                <meta
                    name="description"
                    content="Recherchez parmi des milliers de véhicules d'occasion et neufs. Comparez les prix et les avis pour faire le meilleur choix."
                />
            </Helmet>
            
            <div className="min-h-screen bg-gray-100">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <div className="space-y-8">
                        {/* En-tête */}
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">
                                Rechercher un véhicule
                            </h1>
                            <p className="mt-2 text-sm text-gray-600">
                                Trouvez le véhicule parfait parmi notre large sélection
                            </p>
                        </div>
                        
                        {/* Recherches sauvegardées */}
                        {user && <SavedSearches onSelect={handleSearch} />}
                        
                        {/* Formulaire de recherche */}
                        <div className="bg-white rounded-lg shadow-sm p-6">
                            <SearchForm onSearch={handleSearch} />
                        </div>
                        
                        {/* Résultats */}
                        {searchParams && (
                            <div className="mt-8">
                                <SearchResults searchParams={searchParams} />
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
};

export default Search;
