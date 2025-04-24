import React from 'react';
import { motion } from 'framer-motion';
import {
    ChartBarIcon,
    CurrencyEuroIcon,
    UserGroupIcon,
    ClockIcon,
    TrendingUpIcon,
    TrendingDownIcon,
    RefreshIcon
} from '@heroicons/react/outline';
import {
    LineChart,
    Line,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell
} from 'recharts';

const AnalyticsDashboard = ({ data, onRefresh, dateRange, onDateRangeChange }) => {
    const {
        subscriptionStats,
        tokenStats,
        revenueStats,
        userStats,
        usageStats
    } = data;

    const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444'];

    const StatCard = ({ title, value, change, icon: Icon, color }) => (
        <motion.div
            whileHover={{ y: -2 }}
            className="bg-white rounded-lg shadow-sm p-6"
        >
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm text-gray-600 mb-1">{title}</p>
                    <h3 className="text-2xl font-bold text-gray-900">{value}</h3>
                </div>
                <div className={`h-12 w-12 rounded-lg ${color} bg-opacity-10 flex items-center justify-center`}>
                    <Icon className={`h-6 w-6 ${color}`} />
                </div>
            </div>
            <div className="mt-4 flex items-center">
                <div className={`flex items-center ${
                    change >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                    {change >= 0 ? (
                        <TrendingUpIcon className="h-4 w-4 mr-1" />
                    ) : (
                        <TrendingDownIcon className="h-4 w-4 mr-1" />
                    )}
                    <span className="font-medium">
                        {Math.abs(change)}%
                    </span>
                </div>
                <span className="text-gray-500 text-sm ml-2">vs période précédente</span>
            </div>
        </motion.div>
    );

    return (
        <div className="space-y-6">
            {/* En-tête */}
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900">
                    Tableau de bord
                </h2>
                <div className="flex items-center space-x-4">
                    <select
                        value={dateRange}
                        onChange={(e) => onDateRangeChange(e.target.value)}
                        className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="7d">7 derniers jours</option>
                        <option value="30d">30 derniers jours</option>
                        <option value="90d">90 derniers jours</option>
                        <option value="1y">Cette année</option>
                    </select>
                    <button
                        onClick={onRefresh}
                        className="p-2 text-gray-600 hover:text-gray-900"
                    >
                        <RefreshIcon className="h-5 w-5" />
                    </button>
                </div>
            </div>

            {/* Cartes statistiques */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Revenus mensuels"
                    value={`${revenueStats.monthly}€`}
                    change={revenueStats.change}
                    icon={CurrencyEuroIcon}
                    color="text-green-600"
                />
                <StatCard
                    title="Abonnés actifs"
                    value={subscriptionStats.activeUsers}
                    change={subscriptionStats.change}
                    icon={UserGroupIcon}
                    color="text-blue-600"
                />
                <StatCard
                    title="Jetons utilisés"
                    value={tokenStats.used}
                    change={tokenStats.change}
                    icon={ChartBarIcon}
                    color="text-purple-600"
                />
                <StatCard
                    title="Temps moyen d'utilisation"
                    value={`${usageStats.averageTime}min`}
                    change={usageStats.change}
                    icon={ClockIcon}
                    color="text-orange-600"
                />
            </div>

            {/* Graphiques */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Revenus */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Évolution des revenus
                    </h3>
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={revenueStats.history}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="date" />
                                <YAxis />
                                <Tooltip />
                                <Line
                                    type="monotone"
                                    dataKey="value"
                                    stroke="#3B82F6"
                                    strokeWidth={2}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Distribution des abonnements */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Distribution des abonnements
                    </h3>
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={subscriptionStats.distribution}
                                    innerRadius={60}
                                    outerRadius={100}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {subscriptionStats.distribution.map((entry, index) => (
                                        <Cell
                                            key={`cell-${index}`}
                                            fill={COLORS[index % COLORS.length]}
                                        />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                        <div className="mt-4 grid grid-cols-2 gap-4">
                            {subscriptionStats.distribution.map((item, index) => (
                                <div
                                    key={item.name}
                                    className="flex items-center space-x-2"
                                >
                                    <div
                                        className="h-3 w-3 rounded-full"
                                        style={{ backgroundColor: COLORS[index % COLORS.length] }}
                                    />
                                    <span className="text-sm text-gray-600">
                                        {item.name} ({item.value}%)
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Utilisation des jetons */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Utilisation des jetons par fonctionnalité
                    </h3>
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={tokenStats.usageByFeature}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Bar dataKey="value" fill="#3B82F6" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Activité utilisateur */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Activité utilisateur
                    </h3>
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={userStats.activity}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="date" />
                                <YAxis />
                                <Tooltip />
                                <Line
                                    type="monotone"
                                    dataKey="active"
                                    stroke="#10B981"
                                    strokeWidth={2}
                                    name="Utilisateurs actifs"
                                />
                                <Line
                                    type="monotone"
                                    dataKey="new"
                                    stroke="#F59E0B"
                                    strokeWidth={2}
                                    name="Nouveaux utilisateurs"
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Métriques détaillées */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Taux de conversion */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Taux de conversion
                    </h3>
                    <div className="text-3xl font-bold text-blue-600 mb-2">
                        {userStats.conversionRate}%
                    </div>
                    <p className="text-sm text-gray-600">
                        Des utilisateurs gratuits passent à un abonnement payant
                    </p>
                </div>

                {/* Taux de rétention */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Taux de rétention
                    </h3>
                    <div className="text-3xl font-bold text-green-600 mb-2">
                        {userStats.retentionRate}%
                    </div>
                    <p className="text-sm text-gray-600">
                        Des abonnés renouvellent leur abonnement
                    </p>
                </div>

                {/* Revenu moyen par utilisateur */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                        ARPU
                    </h3>
                    <div className="text-3xl font-bold text-purple-600 mb-2">
                        {revenueStats.arpu}€
                    </div>
                    <p className="text-sm text-gray-600">
                        Revenu moyen par utilisateur
                    </p>
                </div>
            </div>
        </div>
    );
};

export default AnalyticsDashboard;
