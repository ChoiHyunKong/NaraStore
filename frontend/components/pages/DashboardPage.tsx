import React from 'react';
import DashboardWidget from '../DashboardWidget';
import { LayoutDashboard, ArrowRight, FileText } from 'lucide-react';
import { RFP, Todo } from '../../types';

interface DashboardPageProps {
    rfps: RFP[];
    todos: Todo[];
    onNavigateToAnalysis: () => void;
}

const DashboardPage: React.FC<DashboardPageProps> = ({ rfps, todos, onNavigateToAnalysis }) => {
    return (
        <div className="flex-1 p-8 max-w-[1600px] mx-auto w-full">
            <div className="mb-8 flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-gray-800">대시보드 개요</h2>
                    <p className="text-slate-500 mt-1">제안서 분석 현황과 할 일 목록을 한눈에 확인하세요.</p>
                </div>
                <button
                    onClick={onNavigateToAnalysis}
                    className="flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-lg shadow-indigo-200 transition-all active:scale-[0.98]"
                >
                    <FileText className="w-5 h-5" />
                    제안서 분석 하러가기
                    <ArrowRight className="w-4 h-4" />
                </button>
            </div>

            {/* Existing Dashboard Widget */}
            <DashboardWidget rfps={rfps} todos={todos} />

            {/* Additional Dashboard Content Placeholders */}
            <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="bg-white p-6 rounded-3xl shadow-sm border border-indigo-50">
                    <h3 className="text-lg font-bold text-gray-800 mb-4">최근 분석 활동</h3>
                    <div className="h-40 flex items-center justify-center text-gray-400 bg-gray-50 rounded-2xl border border-dashed border-gray-200">
                        활동 로그 준비 중...
                    </div>
                </div>
                <div className="bg-white p-6 rounded-3xl shadow-sm border border-indigo-50">
                    <h3 className="text-lg font-bold text-gray-800 mb-4">시스템 상태</h3>
                    <div className="h-40 flex items-center justify-center text-gray-400 bg-gray-50 rounded-2xl border border-dashed border-gray-200">
                        시스템 모니터링 준비 중...
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DashboardPage;
