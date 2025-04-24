import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    UserGroupIcon,
    PlusIcon,
    UserCircleIcon,
    CogIcon,
    TrashIcon,
    LightningBoltIcon
} from '@heroicons/react/outline';

const FamilyPlan = ({ familyPlan, onAddMember, onRemoveMember, onUpdateAllowance }) => {
    const [showInvite, setShowInvite] = useState(false);
    const [email, setEmail] = useState('');
    const [role, setRole] = useState('ADULT');

    const handleInvite = () => {
        onAddMember({ email, role });
        setEmail('');
        setShowInvite(false);
    };

    const getRoleColor = (role) => {
        switch (role) {
            case 'OWNER':
                return 'text-purple-600 bg-purple-100';
            case 'ADULT':
                return 'text-blue-600 bg-blue-100';
            case 'TEEN':
                return 'text-green-600 bg-green-100';
            case 'CHILD':
                return 'text-orange-600 bg-orange-100';
            default:
                return 'text-gray-600 bg-gray-100';
        }
    };

    return (
        <div className="space-y-6">
            {/* En-tête du plan familial */}
            <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center">
                        <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                            <UserGroupIcon className="h-6 w-6 text-blue-600" />
                        </div>
                        <div>
                            <h2 className="text-xl font-bold text-gray-900">
                                {familyPlan.name}
                            </h2>
                            <p className="text-gray-600">
                                Plan {familyPlan.plan} - {familyPlan.members.length} membres
                            </p>
                        </div>
                    </div>
                    <button
                        onClick={() => setShowInvite(true)}
                        className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                    >
                        <PlusIcon className="h-5 w-5 mr-2" />
                        Ajouter un membre
                    </button>
                </div>

                {/* Modal d'invitation */}
                <AnimatePresence>
                    {showInvite && (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="fixed inset-0 z-50 flex items-center justify-center"
                        >
                            <div className="absolute inset-0 bg-black bg-opacity-50" />
                            <div className="relative bg-white rounded-lg p-6 w-full max-w-md">
                                <h3 className="text-lg font-medium text-gray-900 mb-4">
                                    Inviter un membre
                                </h3>
                                <div className="space-y-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Email
                                        </label>
                                        <input
                                            type="email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                                            placeholder="email@exemple.com"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Rôle
                                        </label>
                                        <select
                                            value={role}
                                            onChange={(e) => setRole(e.target.value)}
                                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                                        >
                                            <option value="ADULT">Adulte</option>
                                            <option value="TEEN">Adolescent</option>
                                            <option value="CHILD">Enfant</option>
                                        </select>
                                    </div>
                                    <div className="flex justify-end space-x-3">
                                        <button
                                            onClick={() => setShowInvite(false)}
                                            className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
                                        >
                                            Annuler
                                        </button>
                                        <button
                                            onClick={handleInvite}
                                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                                        >
                                            Inviter
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Jetons partagés */}
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg mb-6">
                    <div>
                        <h3 className="font-medium text-gray-900">Jetons partagés</h3>
                        <p className="text-sm text-gray-600">
                            Utilisables par tous les membres
                        </p>
                    </div>
                    <div className="text-right">
                        <div className="text-2xl font-bold text-blue-600">
                            {familyPlan.sharedTokens}
                        </div>
                        <div className="text-sm text-gray-600">jetons</div>
                    </div>
                </div>

                {/* Liste des membres */}
                <div className="space-y-4">
                    {familyPlan.members.map((member) => (
                        <motion.div
                            key={member.userId}
                            layout
                            className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                        >
                            <div className="flex items-center">
                                <UserCircleIcon className="h-10 w-10 text-gray-400 mr-3" />
                                <div>
                                    <div className="flex items-center">
                                        <span className="font-medium text-gray-900 mr-2">
                                            {member.userId}
                                        </span>
                                        <span className={`text-xs px-2 py-1 rounded-full ${getRoleColor(member.role)}`}>
                                            {member.role}
                                        </span>
                                    </div>
                                    <div className="text-sm text-gray-600">
                                        Membre depuis le {new Date(member.joinDate).toLocaleDateString()}
                                    </div>
                                </div>
                            </div>
                            <div className="flex items-center space-x-4">
                                <div className="text-right">
                                    <div className="text-sm text-gray-600">Jetons personnels</div>
                                    <div className="font-medium text-gray-900">
                                        {familyPlan.individualTokens[member.userId] || 0}
                                    </div>
                                </div>
                                {member.role !== 'OWNER' && (
                                    <div className="flex space-x-2">
                                        <button
                                            onClick={() => onUpdateAllowance(member.userId)}
                                            className="p-2 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-blue-50"
                                        >
                                            <CogIcon className="h-5 w-5" />
                                        </button>
                                        <button
                                            onClick={() => onRemoveMember(member.userId)}
                                            className="p-2 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50"
                                        >
                                            <TrashIcon className="h-5 w-5" />
                                        </button>
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Statistiques d'utilisation */}
            <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Utilisation des jetons
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {Object.entries(
                        familyPlan.members.reduce((acc, member) => ({
                            ...acc,
                            [member.userId]: Math.floor(Math.random() * 100)  // Exemple de données
                        }), {})
                    ).map(([userId, usage]) => (
                        <div key={userId} className="p-4 bg-gray-50 rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm font-medium text-gray-900">
                                    {userId}
                                </span>
                                <span className="text-sm text-gray-600">
                                    {usage}%
                                </span>
                            </div>
                            <div className="h-2 bg-gray-200 rounded-full">
                                <div
                                    className="h-2 bg-blue-600 rounded-full"
                                    style={{ width: `${usage}%` }}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default FamilyPlan;
