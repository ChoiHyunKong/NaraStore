import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
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

    // 데이터 존재 여부 확인
    const hasData = data && data.length > 0 && data.some(d => d.count > 0);

    // 빈 데이터 생성 (placeholder)
    const generateEmptyData = (currentPeriod: PeriodType) => {
        const count = currentPeriod === '7days' ? 7 : currentPeriod === '1month' ? 30 : 12;
        return Array.from({ length: count }).map((_, i) => ({
            date: i.toString(),
            count: 0
        }));
    };

    const chartData = hasData ? data : generateEmptyData(period);

    // 커스텀 툴팁
    const CustomTooltip = ({ active, payload, label }: any) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-slate-900/90 backdrop-blur-md px-4 py-3 rounded-2xl shadow-2xl border border-slate-700/50">
                    <p className="text-xs font-medium text-slate-400 mb-1">{label}</p>
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.6)]"></div>
                        <p className="text-lg font-black text-white">
                            {payload[0].value} <span className="text-xs font-medium text-slate-500">건</span>
                        </p>
                    </div>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="bg-white rounded-3xl p-6 border border-slate-100 shadow-sm relative overflow-hidden group">
            {/* Background Decoration */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-50/50 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>

            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8 relative z-10">
                <div>
                    <h3 className="text-lg font-black text-slate-800 flex items-center gap-2">
                        활동 분석
                        {!hasData && <span className="text-[10px] font-bold bg-slate-100 text-slate-400 px-2 py-0.5 rounded-full">데이터 없음</span>}
                    </h3>
                    <p className="text-xs font-medium text-slate-400 mt-0.5">기간별 제안서 분석 추이</p>
                </div>
                <div className="flex bg-slate-100 p-1 rounded-xl">
                    {periods.map(({ value, label }) => (
                        <button
                            key={value}
                            onClick={() => onPeriodChange(value)}
                            className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${period === value
                                ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-black/5'
                                : 'text-slate-400 hover:text-slate-600'
                                }`}
                        >
                            {label}
                        </button>
                    ))}
                </div>
            </div>

            {/* Chart */}
            <div className="h-[280px] w-full relative z-10 -ml-4">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                        <defs>
                            <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                        <XAxis
                            dataKey="date"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fontSize: 11, fill: '#94a3b8', fontWeight: 600 }}
                            dy={10}
                            minTickGap={30}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={{ fontSize: 11, fill: '#94a3b8', fontWeight: 600 }}
                            allowDecimals={false}
                        />
                        <Tooltip
                            content={<CustomTooltip />}
                            cursor={{ stroke: '#6366f1', strokeWidth: 1, strokeDasharray: '4 4' }}
                        />
                        <Area
                            type="monotone"
                            dataKey="count"
                            stroke="#4f46e5"
                            strokeWidth={3}
                            fillOpacity={1}
                            fill="url(#colorCount)"
                            animationDuration={1500}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default ActivityChart;
