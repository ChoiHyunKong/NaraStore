import React from 'react';

interface ProgressBarProps {
    percentage: number; // 0-1 (0% to 100%)
    label?: string;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ percentage, label }) => {
    const displayPercentage = Math.round(percentage * 100);

    return (
        <div className="bg-gradient-to-br from-indigo-50/50 to-violet-50/50 border border-indigo-100 rounded-2xl p-4">
            <div className="flex items-center justify-between mb-2">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                    {label || 'Todo 완료율'}
                </p>
                <p className="text-2xl font-extrabold text-indigo-600">{displayPercentage}%</p>
            </div>
            <div className="relative w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                <div
                    className="absolute inset-y-0 left-0 bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full transition-all duration-1000 ease-out"
                    style={{ width: `${displayPercentage}%` }}
                >
                    {/* Shimmer effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer"></div>
                </div>
            </div>
        </div>
    );
};

export default ProgressBar;
