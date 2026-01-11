import React from 'react';
import DashboardWidget from '../DashboardWidget';
import { LayoutDashboard, ArrowRight, FileText } from 'lucide-react';
import { RFP, TodoItem } from '../../types';
import Footer from '../footer/Footer';

interface DashboardPageProps {
    rfps: RFP[];
    todos: TodoItem[];
    onNavigateToAnalysis: () => void;
}

const DashboardPage: React.FC<DashboardPageProps> = ({ rfps, todos, onNavigateToAnalysis }) => {
    return (
        <div className="flex flex-col w-full h-full">
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
            </div>

            <div className="mt-24">
                <Footer />
            </div>
        </div>
    );
};

export default DashboardPage;
