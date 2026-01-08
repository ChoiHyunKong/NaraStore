import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ActivityData, PeriodType } from '../../types';

interface ActivityChartProps {
    data: ActivityData[];
    period: PeriodType;
    onPeriodChange: (period: PeriodType) => void;
}

const ActivityChart: React.FC<ActivityChartProps> = ({ data, period, onPeriodChange }) => {
    const periods: { value: PeriodType; label: string }[] = [
        { value: '7days', label: '7일' },
        { value: '1month', label: '1개월' },
        { value: '1year', label: '1년' }
    ];

    // 차트 타입 결정 (1년은 Line, 나머지는 Bar)
    const isLineChart = period === '1year';

    return (
        <div className="bg-gradient-to-br from-indigo-50/50 to-violet-50/50 border border-indigo-100 rounded-2xl p-4">
            {/* Header with Period Tabs */}
            <div className="flex items-center justify-between mb-4">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide">활동 추이</p>
                <div className="flex bg-white/80 p-1 rounded-lg shadow-sm">
                    {periods.map(({ value, label }) => (
                        <button
                            key={value}
                            onClick={() => onPeriodChange(value)}
                            className={`px-3 py-1 rounded-md text-xs font-bold transition-all ${period === value
                                    ? 'bg-indigo-600 text-white shadow-sm'
                                    : 'text-gray-500 hover:text-gray-700'
                                }`}
                        >
                            {label}
                        </button>
                    ))}
                </div>
            </div>

            {/* Chart */}
            <div className="h-40">
                <ResponsiveContainer width="100%" height="100%">
                    {isLineChart ? (
                        <LineChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                            <XAxis
                                dataKey="date"
                                tick={{ fontSize: 10, fill: '#9CA3AF' }}
                                stroke="#D1D5DB"
                            />
                            <YAxis
                                tick={{ fontSize: 10, fill: '#9CA3AF' }}
                                stroke="#D1D5DB"
                            />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: 'rgba(255,255,255,0.95)',
                                    border: '1px solid #E0E7FF',
                                    borderRadius: '8px',
                                    fontSize: '12px'
                                }}
                            />
                            <Line
                                type="monotone"
                                dataKey="count"
                                stroke="#4F46E5"
                                strokeWidth={2}
                                dot={{ fill: '#4F46E5', r: 3 }}
                                activeDot={{ r: 5 }}
                            />
                        </LineChart>
                    ) : (
                        <BarChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                            <XAxis
                                dataKey="date"
                                tick={{ fontSize: 10, fill: '#9CA3AF' }}
                                stroke="#D1D5DB"
                            />
                            <YAxis
                                tick={{ fontSize: 10, fill: '#9CA3AF' }}
                                stroke="#D1D5DB"
                            />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: 'rgba(255,255,255,0.95)',
                                    border: '1px solid #E0E7FF',
                                    borderRadius: '8px',
                                    fontSize: '12px'
                                }}
                            />
                            <Bar
                                dataKey="count"
                                fill="url(#colorGradient)"
                                radius={[4, 4, 0, 0]}
                            />
                            <defs>
                                <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stopColor="#4F46E5" stopOpacity={0.8} />
                                    <stop offset="100%" stopColor="#8B5CF6" stopOpacity={0.6} />
                                </linearGradient>
                            </defs>
                        </BarChart>
                    )}
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default ActivityChart;
