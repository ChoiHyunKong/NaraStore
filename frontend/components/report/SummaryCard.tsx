import React from 'react';
import { AnalysisSummary } from '../../types';
import { Calendar, CheckCircle2, DollarSign, FileText } from 'lucide-react';

interface SummaryCardProps {
    summary: AnalysisSummary;
}

const SummaryCard: React.FC<SummaryCardProps> = ({ summary }) => {
    return (
        <div className="space-y-6 animate-in slide-in-from-bottom duration-500">
            {/* Overview Card */}
            <div className="bg-gradient-to-br from-indigo-50 to-white border border-indigo-100 rounded-2xl p-6 shadow-sm">
                <h3 className="text-xl font-bold text-indigo-900 mb-2">{summary.project_name}</h3>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
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
