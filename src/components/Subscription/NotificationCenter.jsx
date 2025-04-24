import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    BellIcon,
    ExclamationIcon,
    CheckCircleIcon,
    InformationCircleIcon,
    XIcon
} from '@heroicons/react/outline';

const NotificationCenter = ({ notifications, onMarkAsRead, onClearAll }) => {
    const [showAll, setShowAll] = useState(false);
    const [isOpen, setIsOpen] = useState(false);

    const unreadCount = notifications.filter(n => !n.read).length;

    const getNotificationIcon = (type) => {
        switch (type) {
            case 'WARNING':
                return <ExclamationIcon className="h-5 w-5 text-yellow-500" />;
            case 'SUCCESS':
                return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
            case 'ERROR':
                return <ExclamationIcon className="h-5 w-5 text-red-500" />;
            default:
                return <InformationCircleIcon className="h-5 w-5 text-blue-500" />;
        }
    };

    const getNotificationStyle = (type) => {
        switch (type) {
            case 'WARNING':
                return 'bg-yellow-50 border-yellow-100';
            case 'SUCCESS':
                return 'bg-green-50 border-green-100';
            case 'ERROR':
                return 'bg-red-50 border-red-100';
            default:
                return 'bg-blue-50 border-blue-100';
        }
    };

    return (
        <div className="relative">
            {/* Bouton de notification */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="relative p-2 text-gray-600 hover:text-gray-900 focus:outline-none"
            >
                <BellIcon className="h-6 w-6" />
                {unreadCount > 0 && (
                    <span className="absolute top-0 right-0 transform translate-x-1/2 -translate-y-1/2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                        {unreadCount}
                    </span>
                )}
            </button>

            {/* Panel de notifications */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-lg shadow-lg z-50"
                    >
                        <div className="p-4 border-b border-gray-200">
                            <div className="flex items-center justify-between">
                                <h3 className="text-lg font-medium text-gray-900">
                                    Notifications
                                </h3>
                                <div className="flex items-center space-x-2">
                                    <button
                                        onClick={onClearAll}
                                        className="text-sm text-gray-600 hover:text-gray-900"
                                    >
                                        Tout effacer
                                    </button>
                                    <button
                                        onClick={() => setIsOpen(false)}
                                        className="text-gray-400 hover:text-gray-500"
                                    >
                                        <XIcon className="h-5 w-5" />
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div className="max-h-96 overflow-y-auto">
                            {notifications.length === 0 ? (
                                <div className="p-4 text-center text-gray-500">
                                    Aucune notification
                                </div>
                            ) : (
                                <div className="divide-y divide-gray-200">
                                    {notifications
                                        .slice(0, showAll ? undefined : 5)
                                        .map((notification) => (
                                            <motion.div
                                                key={notification.id}
                                                layout
                                                initial={{ opacity: 0 }}
                                                animate={{ opacity: 1 }}
                                                exit={{ opacity: 0 }}
                                                className={`p-4 ${
                                                    notification.read
                                                        ? 'bg-white'
                                                        : getNotificationStyle(notification.type)
                                                } transition-colors duration-200`}
                                                onClick={() => onMarkAsRead(notification.id)}
                                            >
                                                <div className="flex items-start">
                                                    <div className="flex-shrink-0">
                                                        {getNotificationIcon(notification.type)}
                                                    </div>
                                                    <div className="ml-3 flex-1">
                                                        <p className="text-sm font-medium text-gray-900">
                                                            {notification.title}
                                                        </p>
                                                        <p className="mt-1 text-sm text-gray-600">
                                                            {notification.message}
                                                        </p>
                                                        <div className="mt-2 text-xs text-gray-500">
                                                            {new Date(
                                                                notification.timestamp
                                                            ).toLocaleString()}
                                                        </div>
                                                    </div>
                                                </div>
                                            </motion.div>
                                        ))}
                                </div>
                            )}
                        </div>

                        {notifications.length > 5 && !showAll && (
                            <div className="p-4 border-t border-gray-200">
                                <button
                                    onClick={() => setShowAll(true)}
                                    className="text-sm text-blue-600 hover:text-blue-700"
                                >
                                    Voir toutes les notifications
                                </button>
                            </div>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default NotificationCenter;
