import React from 'react';
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

    // 데이터가 없는 경우 처리
    const hasData = data && data.length > 0 && data.some(d => d.count > 0);

    // Placeholder data generator
    const generateEmptyData = (currentPeriod: PeriodType) => {
        const count = currentPeriod === '7days' ? 7 : currentPeriod === '1month' ? 30 : 12;
        return Array.from({ length: count }).map((_, i) => ({
            date: i.toString(),
            count: 0
        }));
    };

    // 커스텀 툴팁 (Memozied to prevent re-renders)
    const CustomTooltip = React.memo(({ active, payload, label }: any) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-white/95 border border-indigo-100 p-3 rounded-xl shadow-lg shadow-indigo-100/20">
                    <p className="text-xs font-semibold text-gray-500 mb-1">{label}</p>
                    <p className="text-sm font-bold text-indigo-600">
                        {payload[0].value}건
                    </p>
                </div>
            );
        }
        return null;
    });

    return (
        <div className="bg-gradient-to-br from-indigo-50/50 to-violet-50/50 border border-indigo-100 rounded-2xl p-6 transition-all hover:shadow-lg hover:shadow-indigo-100/40">
            {/* Header with Period Tabs */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <div>
                    <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Activity Trends</p>
                    <h3 className="text-lg font-bold text-gray-800">활동 추이</h3>
                </div>
                <div className="flex bg-white/60 backdrop-blur-md p-1.5 rounded-xl border border-white/50 shadow-sm">
                    {periods.map(({ value, label }) => (
                        <button
                            key={value}
                            onClick={() => onPeriodChange(value)}
                            className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all duration-300 ${period === value
                                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200'
                                : 'text-gray-500 hover:text-gray-700 hover:bg-white/50'
                                }`}
                        >
                            {label}
                        </button>
                    ))}
                </div>
            </div>

            {/* Chart Container */}
            <div className="h-64 relative w-full">
                <div className="relative w-full h-full">
                    <ResponsiveContainer width="100%" height="100%">
                        {isLineChart ? (
                            <LineChart data={hasData ? data : generateEmptyData(period)} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="lineColorGradient" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#ec4899" stopOpacity={0.2} />
                                        <stop offset="95%" stopColor="#ec4899" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" vertical={false} />
                                <XAxis
                                    dataKey="date"
                                    tick={{ fontSize: 11, fill: '#9CA3AF', fontWeight: 500 }}
                                    stroke="#E5E7EB"
                                    tickLine={false}
                                    axisLine={false}
                                    dy={10}
                                    minTickGap={30}
                                />
                                <YAxis
                                    tick={{ fontSize: 11, fill: '#9CA3AF', fontWeight: 500 }}
                                    stroke="#E5E7EB"
                                    tickLine={false}
                                    axisLine={false}
                                    allowDecimals={false}
                                    dx={-10}
                                />
                                <Tooltip
                                    content={<CustomTooltip />}
                                    cursor={false} // [Optimization] 마우스 추적 라인 제거 (lag 감소)
                                    isAnimationActive={false} // [Optimization] 툴팁 애니메이션 제거
                                />
                                <Line
                                    type="monotone"
                                    dataKey="count"
                                    stroke={hasData ? "#ec4899" : "#E5E7EB"} // 데이터 없으면 회색 선
                                    strokeWidth={3}
                                    dot={hasData ? { fill: '#ec4899', r: 4, strokeWidth: 2, stroke: '#fff' } : false}
                                    activeDot={hasData ? { r: 6, strokeWidth: 0 } : false}
                                    animationDuration={1500}
                                />
                            </LineChart>
                        ) : (
                            <BarChart data={hasData ? data : generateEmptyData(period)} margin={{ top: 10, right: 10, left: -20, bottom: 0 }} barSize={period === '7days' ? 32 : 12}>
                                <defs>
                                    <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="0%" stopColor="#6366f1" stopOpacity={1} />
                                        <stop offset="100%" stopColor="#818cf8" stopOpacity={0.6} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" vertical={false} />
                                <XAxis
                                    dataKey="date"
                                    tick={{ fontSize: 11, fill: '#9CA3AF', fontWeight: 500 }}
                                    stroke="#E5E7EB"
                                    tickLine={false}
                                    axisLine={false}
                                    dy={10}
                                    interval={period === '1month' ? 4 : 0}
                                />
                                <YAxis
                                    tick={{ fontSize: 11, fill: '#9CA3AF', fontWeight: 500 }}
                                    stroke="#E5E7EB"
                                    tickLine={false}
                                    axisLine={false}
                                    allowDecimals={false}
                                    dx={-10}
                                />
                                <Tooltip
                                    content={<CustomTooltip />}
                                    cursor={{ fill: 'transparent' }} // [Optimization] 마우스 호버 시 배경바 제거
                                    isAnimationActive={false}
                                />
                                <Bar
                                    dataKey="count"
                                    fill={hasData ? "url(#barGradient)" : "#F3F4F6"} // 데이터 유무에 따른 색상 처리
                                    radius={[6, 6, 0, 0]}
                                    animationDuration={1500}
                                />
                            </BarChart>
                        )}
                    </ResponsiveContainer>

                    {/* No Data Overlay */}
                    {!hasData && (
                        <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-400 bg-white/50 backdrop-blur-[1px] rounded-xl z-10">
                            <div className="p-4 bg-white/80 rounded-2xl shadow-sm border border-indigo-50 flex flex-col items-center">
                                <p className="text-sm font-bold text-gray-600">데이터가 없습니다</p>
                                <p className="text-xs mt-1 text-gray-400">새로운 활동을 시작해보세요</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ActivityChart;
