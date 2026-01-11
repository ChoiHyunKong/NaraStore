import { RFP, TodoItem, DashboardStats, PeriodType, ActivityData } from '../types';

/**
 * Dashboard Service
 * Firebase 데이터로부터 대시보드 통계를 계산하는 서비스
 */

/**
 * RFP 및 Todo 데이터로부터 대시보드 통계 계산
 */
export const calculateStats = (rfps: RFP[], todos: TodoItem[]): DashboardStats => {
    // 상태별 개수 계산
    const totalRFPs = rfps.length;
    const completedCount = rfps.filter(r => r.status === 'completed').length;
    const pendingCount = rfps.filter(r => r.status === 'pending').length;
    const errorCount = rfps.filter(r => r.status === 'error').length;

    // Todo 완료율 계산
    const totalTodos = todos.length;
    const completedTodos = todos.filter(t => t.completed).length;
    const todoCompletionRate = totalTodos > 0 ? completedTodos / totalTodos : 0;

    return {
        totalRFPs,
        completedCount,
        pendingCount,
        errorCount,
        todoCompletionRate,
        activityData: [] // 나중에 계산
    };
};

/**
 * 기간별 활동 데이터 생성
 */
export const getActivityData = (rfps: RFP[], period: PeriodType): ActivityData[] => {
    const now = new Date();
    const activityMap = new Map<string, number>();

    if (period === '7days') {
        // 최근 7일 데이터 (일별)
        for (let i = 6; i >= 0; i--) {
            const date = new Date(now);
            date.setDate(date.getDate() - i);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            const dateKey = `${year}-${month}-${day}`;
            activityMap.set(dateKey, 0);
        }

        // RFP의 analysisDate를 기준으로 집계
        rfps.forEach(rfp => {
            if (rfp.analysisDate && activityMap.has(rfp.analysisDate)) {
                activityMap.set(rfp.analysisDate, (activityMap.get(rfp.analysisDate) || 0) + 1);
            }
        });

        return Array.from(activityMap.entries()).map(([date, count]) => ({
            date: formatDateLabel(date, '7days'),
            count
        }));

    } else if (period === '1month') {
        // 최근 30일 데이터 (일별)
        for (let i = 29; i >= 0; i--) {
            const date = new Date(now);
            date.setDate(date.getDate() - i);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            const dateKey = `${year}-${month}-${day}`;
            activityMap.set(dateKey, 0);
        }

        rfps.forEach(rfp => {
            if (rfp.analysisDate && activityMap.has(rfp.analysisDate)) {
                activityMap.set(rfp.analysisDate, (activityMap.get(rfp.analysisDate) || 0) + 1);
            }
        });

        return Array.from(activityMap.entries()).map(([date, count]) => ({
            date: formatDateLabel(date, '1month'),
            count
        }));

    } else {
        // 최근 12개월 데이터 (월별)
        for (let i = 11; i >= 0; i--) {
            const date = new Date(now);
            date.setMonth(date.getMonth() - i);
            const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
            activityMap.set(monthKey, 0);
        }

        rfps.forEach(rfp => {
            if (rfp.analysisDate) {
                const monthKey = rfp.analysisDate.substring(0, 7); // YYYY-MM
                if (activityMap.has(monthKey)) {
                    activityMap.set(monthKey, (activityMap.get(monthKey) || 0) + 1);
                }
            }
        });

        return Array.from(activityMap.entries()).map(([date, count]) => ({
            date: formatDateLabel(date, '1year'),
            count
        }));
    }
};

/**
 * 날짜 라벨 포맷팅
 */
const formatDateLabel = (dateStr: string, period: PeriodType): string => {
    if (period === '7days') {
        // "월/일" 형식
        const date = new Date(dateStr);
        return `${date.getMonth() + 1}/${date.getDate()}`;
    } else if (period === '1month') {
        // "MM/DD" 형식
        const parts = dateStr.split('-');
        return `${parts[1]}/${parts[2]}`;
    } else {
        // "YYYY년 M월" 형식
        const [year, month] = dateStr.split('-');
        return `${year}년 ${parseInt(month)}월`;
    }
};

export const dashboardService = {
    calculateStats,
    getActivityData
};
