import React, { useState, useEffect, useMemo } from 'react';
import { ChevronDown, ChevronUp, BarChart3 } from 'lucide-react';
import { RFP, TodoItem, PeriodType } from '../types';
import { calculateStats, getActivityData } from '../services/dashboardService';
import StatCard from './dashboard/StatCard';
import ActivityChart from './dashboard/ActivityChart';

import { FileText, CheckCircle2, Clock, AlertCircle } from 'lucide-react';

interface DashboardWidgetProps {
    rfps: RFP[];
    todos: TodoItem[];
}

const DashboardWidget: React.FC<DashboardWidgetProps> = ({ rfps, todos }) => {
    const [isExpanded, setIsExpanded] = useState(() => {
        const saved = localStorage.getItem('dashboard_expanded');
        return saved !== null ? JSON.parse(saved) : false;
    });

    const [period, setPeriod] = useState<PeriodType>(() => {
        const saved = localStorage.getItem('dashboard_period');
        return (saved as PeriodType) || '7days';
    });

    // 확장 상태를 로컬 스토리지에 저장
    useEffect(() => {
        localStorage.setItem('dashboard_expanded', JSON.stringify(isExpanded));
    }, [isExpanded]);

    // 기간 선택을 로컬 스토리지에 저장
    useEffect(() => {
        localStorage.setItem('dashboard_period', period);
    }, [period]);

    // 통계 계산 (메모이제이션)
    const stats = useMemo(() => calculateStats(rfps, todos), [rfps, todos]);

    // 활동 데이터 계산 (메모이제이션)
    const activityData = useMemo(() => getActivityData(rfps, period), [rfps, period]);

    const handleToggle = () => {
        setIsExpanded(!isExpanded);
    };

    return (
        <div className="glass-card rounded-3xl shadow-xl shadow-indigo-100/50 overflow-hidden border-indigo-50/50 transition-all">
            {/* Header */}
            <div
                className="flex items-center justify-between p-5 cursor-pointer hover:bg-white/40 transition-colors border-b border-gray-100/50"
                onClick={handleToggle}
            >
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center shadow-md">
                        <BarChart3 className="w-4 h-4 text-white" />
                    </div>
                    <h2 className="text-base font-bold text-gray-800">분석 현황</h2>
                </div>
                <div className="flex items-center gap-3">
                    {/* Quick Stats (Collapsed) */}
                    {!isExpanded && (
                        <div className="flex items-center gap-2 text-xs font-medium text-gray-500">
                            <span className="flex items-center gap-1">
                                <FileText className="w-3 h-3" />
                                {stats.totalRFPs}
                            </span>
                            <span className="text-gray-300">|</span>
                            <span className="flex items-center gap-1 text-emerald-600">
                                <CheckCircle2 className="w-3 h-3" />
                                {stats.completedCount}
                            </span>
                        </div>
                    )}
                    <button
                        className="p-1.5 hover:bg-indigo-50 rounded-lg transition-colors"
                        aria-label={isExpanded ? 'Collapse' : 'Expand'}
                    >
                        {isExpanded ? (
                            <ChevronUp className="w-4 h-4 text-gray-600" />
                        ) : (
                            <ChevronDown className="w-4 h-4 text-gray-600" />
                        )}
                    </button>
                </div>
            </div>

            {/* Content (Expandable) */}
            {isExpanded && (
                <div className="p-5 space-y-4 animate-in fade-in slide-in-from-top-2 duration-300">
                    {/* Stat Cards Grid */}
                    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                        <StatCard
                            label="총 RFP"
                            value={stats.totalRFPs}
                            icon={FileText}
                            color="primary"
                        />
                        <StatCard
                            label="완료"
                            value={stats.completedCount}
                            icon={CheckCircle2}
                            color="success"
                        />
                        <StatCard
                            label="진행중"
                            value={stats.pendingCount}
                            icon={Clock}
                            color="warning"
                        />
                        <StatCard
                            label="오류"
                            value={stats.errorCount}
                            icon={AlertCircle}
                            color="error"
                        />
                    </div>

                    {/* Activity Chart */}
                    <ActivityChart
                        data={activityData}
                        period={period}
                        onPeriodChange={setPeriod}
                    />

                </div>
            )}
        </div>
    );
};

export default DashboardWidget;
