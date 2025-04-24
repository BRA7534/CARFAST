import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

const Header = () => {
    const { user, logout } = useAuth();

    return (
        <header className="bg-white shadow-sm">
            <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    {/* Logo et navigation principale */}
                    <div className="flex">
                        <div className="flex-shrink-0 flex items-center">
                            <Link to="/" className="text-2xl font-bold text-blue-600">
                                CarFast
                            </Link>
                        </div>
                        <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                            <Link
                                to="/search"
                                className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                            >
                                Rechercher
                            </Link>
                            <Link
                                to="/compare"
                                className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                            >
                                Comparer
                            </Link>
                            <Link
                                to="/history"
                                className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                            >
                                Historique
                            </Link>
                        </div>
                    </div>

                    {/* Actions utilisateur */}
                    <div className="hidden sm:ml-6 sm:flex sm:items-center">
                        {user ? (
                            <div className="flex items-center space-x-4">
                                <span className="text-sm text-gray-700">
                                    {user.email}
                                </span>
                                <button
                                    onClick={logout}
                                    className="bg-white text-gray-700 hover:bg-gray-50 px-4 py-2 rounded-md text-sm font-medium"
                                >
                                    Déconnexion
                                </button>
                            </div>
                        ) : (
                            <div className="flex items-center space-x-4">
                                <Link
                                    to="/login"
                                    className="bg-white text-gray-700 hover:bg-gray-50 px-4 py-2 rounded-md text-sm font-medium"
                                >
                                    Connexion
                                </Link>
                                <Link
                                    to="/register"
                                    className="bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-md text-sm font-medium"
                                >
                                    Inscription
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </nav>
        </header>
    );
};

export default Header;
