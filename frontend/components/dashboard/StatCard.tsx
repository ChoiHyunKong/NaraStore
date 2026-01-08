import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
    label: string;
    value: number;
    icon: LucideIcon;
    color: 'primary' | 'success' | 'warning' | 'error';
}

const StatCard: React.FC<StatCardProps> = ({ label, value, icon: Icon, color }) => {
    const colorClasses = {
        primary: {
            bg: 'from-indigo-50/50 to-violet-50/50',
            icon: 'text-indigo-600',
            border: 'border-indigo-100',
            text: 'text-indigo-600'
        },
        success: {
            bg: 'from-emerald-50/50 to-green-50/50',
            icon: 'text-emerald-600',
            border: 'border-emerald-100',
            text: 'text-emerald-600'
        },
        warning: {
            bg: 'from-amber-50/50 to-yellow-50/50',
            icon: 'text-amber-600',
            border: 'border-amber-100',
            text: 'text-amber-600'
        },
        error: {
            bg: 'from-red-50/50 to-rose-50/50',
            icon: 'text-red-600',
            border: 'border-red-100',
            text: 'text-red-600'
        }
    };

    const styles = colorClasses[color];

    return (
        <div className={`group relative overflow-hidden bg-gradient-to-br ${styles.bg} border ${styles.border} rounded-2xl p-4 transition-all hover:-translate-y-1 hover:shadow-md cursor-pointer`}>
            <div className="flex items-start justify-between">
                <div>
                    <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">{label}</p>
                    <p className={`text-2xl font-extrabold ${styles.text}`}>{value}</p>
                </div>
                <div className={`w-10 h-10 rounded-xl bg-white/80 flex items-center justify-center ${styles.icon} shadow-sm`}>
                    <Icon className="w-5 h-5" />
                </div>
            </div>
            {/* Subtle hover effect */}
            <div className={`absolute inset-x-0 bottom-0 h-1 ${styles.icon} bg-current opacity-0 group-hover:opacity-20 transition-opacity`}></div>
        </div>
    );
};

export default StatCard;
