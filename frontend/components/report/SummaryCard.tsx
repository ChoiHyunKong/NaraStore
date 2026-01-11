import React from 'react';
import { AnalysisSummary } from '../../types';
import { Calendar, CheckCircle2, DollarSign, FileText } from 'lucide-react';

interface SummaryCardProps {
    summary: AnalysisSummary;
}

const SummaryCard: React.FC<SummaryCardProps> = ({ summary }) => {
    return (
        <div className="space-y-6 animate-in slide-in-from-bottom duration-500">
            {/* Overview & Purpose Section - CLEAN WHITE STYLE */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
                <h3 className="text-xl font-bold mb-2 text-gray-900">{summary.project_name}</h3>

                {/* Key Keywords - HashTag Style */}
                {summary.key_keywords && summary.key_keywords.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-3 mb-6">
                        {summary.key_keywords.map((keyword, idx) => (
                            <span key={idx} className="text-indigo-600 font-bold text-sm bg-indigo-50 px-3 py-1 rounded-full border border-indigo-100">
                                #{keyword}
                            </span>
                        ))}
                    </div>
                )}

                {/* Overview */}
                {summary.overview && (
                    <div className="mt-4">
                        <p className="text-gray-500 text-xs font-bold uppercase tracking-wider mb-2 flex items-center gap-1">
                            <span className="w-1 h-4 bg-indigo-500 rounded-full inline-block"></span>
                            종합 요약
                        </p>
                        <p className="text-sm leading-relaxed text-gray-700">{summary.overview}</p>
                    </div>
                )}

                {/* Purpose */}
                {summary.purpose && (
                    <div className="mt-6 bg-gray-50 rounded-xl p-5 border border-gray-100">
                        <p className="text-gray-500 text-xs font-bold uppercase tracking-wider mb-2">🎯 사업 목적</p>
                        <p className="text-sm leading-relaxed text-gray-800 font-medium">{summary.purpose}</p>
                    </div>
                )}
            </div>

            {/* Meta Info Cards */}
            <div className="bg-gradient-to-br from-indigo-50 to-white border border-indigo-100 rounded-2xl p-6 shadow-sm">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="flex items-center gap-3 bg-white p-3 rounded-xl border border-indigo-50 shadow-sm">
                        <div className="bg-indigo-100 p-2 rounded-lg">
                            <Calendar className="w-5 h-5 text-indigo-600" />
                        </div>
                        <div>
                            <p className="text-xs text-indigo-400 font-semibold mb-0.5">사업 기간</p>
                            <p className="text-sm font-bold text-gray-800">{summary.period}</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3 bg-white p-3 rounded-xl border border-indigo-50 shadow-sm">
                        <div className="bg-indigo-100 p-2 rounded-lg">
                            <DollarSign className="w-5 h-5 text-indigo-600" />
                        </div>
                        <div>
                            <p className="text-xs text-indigo-400 font-semibold mb-0.5">사업 예산</p>
                            <p className="text-sm font-bold text-gray-800">{summary.budget}</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3 bg-white p-3 rounded-xl border border-indigo-50 shadow-sm">
                        <div className="bg-indigo-100 p-2 rounded-lg">
                            <FileText className="w-5 h-5 text-indigo-600" />
                        </div>
                        <div>
                            <p className="text-xs text-indigo-400 font-semibold mb-0.5">요구사항 수</p>
                            <p className="text-sm font-bold text-gray-800">총 {summary.total_requirements_count}개</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Client Priorities - 발주처 중점 포인트 */}
            {summary.client_priorities && summary.client_priorities.length > 0 && (
                <div className="bg-white border border-amber-100 rounded-2xl p-6 shadow-sm">
                    <h4 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4 flex items-center gap-2">
                        <span className="text-amber-500">⭐</span>
                        발주처 중점 포인트
                    </h4>
                    <ul className="space-y-3">
                        {summary.client_priorities.map((priority, idx) => (
                            <li key={idx} className="flex items-start gap-3 p-3 rounded-xl bg-amber-50/50 hover:bg-amber-50 transition-colors border border-amber-100/50">
                                <div className="mt-0.5 min-w-[20px]">
                                    <div className="w-5 h-5 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center text-xs font-bold">
                                        {idx + 1}
                                    </div>
                                </div>
                                <p className="text-sm text-gray-700 leading-relaxed font-medium">{priority}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Expected Effects */}
            <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
                <h4 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                    기대 효과
                </h4>
                <ul className="space-y-3">
                    {summary.expected_effects.map((effect, idx) => (
                        <li key={idx} className="flex items-start gap-3 p-3 rounded-xl bg-gray-50 hover:bg-emerald-50/50 transition-colors">
                            <div className="mt-0.5 min-w-[20px]">
                                <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center text-xs font-bold">
                                    {idx + 1}
                                </div>
                            </div>
                            <p className="text-sm text-gray-700 leading-relaxed font-medium">{effect}</p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default SummaryCard;
