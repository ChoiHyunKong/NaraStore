import React from 'react';
import { StrategyConfig } from '../../types';
import { Target, BookOpen, Zap, Shield, Lightbulb, TrendingUp } from 'lucide-react';

interface StrategyViewProps {
    strategy: StrategyConfig;
}

const StrategyView: React.FC<StrategyViewProps> = ({ strategy }) => {
    return (
        <div className="space-y-8 animate-in slide-in-from-bottom duration-500">

            {/* 3-Column Strategic Insights */}
            <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                    <Lightbulb className="w-6 h-6 text-indigo-600" />
                    전략적 인사이트
                </h2>

                <div className="grid grid-cols-1 gap-6">
                    {/* Anchor Points */}
                    <div className="bg-white border-2 border-indigo-100 rounded-2xl p-6 shadow-sm hover:shadow-lg transition-shadow">
                        <div className="flex items-center gap-2 mb-4">
                            <div className="bg-indigo-100 p-2 rounded-lg">
                                <Target className="w-5 h-5 text-indigo-600" />
                            </div>
                            <h3 className="text-lg font-bold text-indigo-900">앵커 포인트</h3>
                        </div>
                        <p className="text-xs text-gray-500 mb-4">발주처 핵심 요구사항 기반 전략</p>
                        <ul className="space-y-3">
                            {strategy.anchor_points && strategy.anchor_points.length > 0 ? (
                                strategy.anchor_points.map((point, idx) => (
                                    <li key={idx} className="flex items-start gap-2 p-3 rounded-lg bg-indigo-50/50 hover:bg-indigo-50 transition-colors">
                                        <span className="w-5 h-5 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                                            {idx + 1}
                                        </span>
                                        <span className="text-sm text-gray-700 leading-relaxed">{point}</span>
                                    </li>
                                ))
                            ) : (
                                <li className="text-sm text-gray-400 italic">데이터 없음</li>
                            )}
                        </ul>
                    </div>

                    {/* Differentiation */}
                    <div className="bg-white border-2 border-purple-100 rounded-2xl p-6 shadow-sm hover:shadow-lg transition-shadow">
                        <div className="flex items-center gap-2 mb-4">
                            <div className="bg-purple-100 p-2 rounded-lg">
                                <Zap className="w-5 h-5 text-purple-600" />
                            </div>
                            <h3 className="text-lg font-bold text-purple-900">차별화 요소</h3>
                        </div>
                        <p className="text-xs text-gray-500 mb-4">경쟁사 대비 우리의 강점</p>
                        <ul className="space-y-3">
                            {strategy.differentiation && strategy.differentiation.length > 0 ? (
                                strategy.differentiation.map((diff, idx) => (
                                    <li key={idx} className="flex items-start gap-2 p-3 rounded-lg bg-purple-50/50 hover:bg-purple-50 transition-colors">
                                        <span className="w-5 h-5 rounded-full bg-purple-600 text-white flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                                            {idx + 1}
                                        </span>
                                        <span className="text-sm text-gray-700 leading-relaxed">{diff}</span>
                                    </li>
                                ))
                            ) : (
                                <li className="text-sm text-gray-400 italic">데이터 없음</li>
                            )}
                        </ul>
                    </div>

                    {/* Risk Mitigation */}
                    <div className="bg-white border-2 border-amber-100 rounded-2xl p-6 shadow-sm hover:shadow-lg transition-shadow">
                        <div className="flex items-center gap-2 mb-4">
                            <div className="bg-amber-100 p-2 rounded-lg">
                                <Shield className="w-5 h-5 text-amber-600" />
                            </div>
                            <h3 className="text-lg font-bold text-amber-900">리스크 완화</h3>
                        </div>
                        <p className="text-xs text-gray-500 mb-4">사업 수행 리스크 대응 전략</p>
                        <ul className="space-y-3">
                            {strategy.risk_mitigation && strategy.risk_mitigation.length > 0 ? (
                                strategy.risk_mitigation.map((risk, idx) => (
                                    <li key={idx} className="flex items-start gap-2 p-3 rounded-lg bg-amber-50/50 hover:bg-amber-50 transition-colors">
                                        <span className="w-5 h-5 rounded-full bg-amber-600 text-white flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                                            {idx + 1}
                                        </span>
                                        <span className="text-sm text-gray-700 leading-relaxed">{risk}</span>
                                    </li>
                                ))
                            ) : (
                                <li className="text-sm text-gray-400 italic">데이터 없음</li>
                            )}
                        </ul>
                    </div>
                </div>
            </div>

            {/* Winning Strategy */}
            <div>
                <h3 className="text-lg font-bold text-indigo-900 mb-4 flex items-center gap-2">
                    <div className="bg-indigo-100 p-1.5 rounded-lg">
                        <TrendingUp className="w-5 h-5 text-indigo-600" />
                    </div>
                    종합 수주 전략
                </h3>

                <div className="grid gap-4">
                    {strategy.win_strategy && strategy.win_strategy.length > 0 ? (
                        strategy.win_strategy.map((item, idx) => (
                            <div key={idx} className="bg-white border border-indigo-100 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-indigo-200 transition-all group relative overflow-hidden">
                                <div className="absolute top-0 left-0 w-1 h-full bg-indigo-500"></div>
                                <span className="absolute top-4 right-4 text-xs font-black text-indigo-100 text-[40px] leading-none -z-0 opacity-50 select-none group-hover:opacity-100 transition-opacity">
                                    {idx + 1}
                                </span>
                                <p className="text-gray-700 font-medium leading-relaxed relative z-10 group-hover:text-indigo-900 transition-colors">
                                    {item}
                                </p>
                            </div>
                        ))
                    ) : (
                        <p className="text-gray-400 italic">데이터 없음</p>
                    )}
                </div>
            </div>

            {/* References */}
            {strategy.references && strategy.references.length > 0 && (
                <div>
                    <h3 className="text-lg font-bold text-emerald-900 mb-4 flex items-center gap-2">
                        <div className="bg-emerald-100 p-1.5 rounded-lg">
                            <BookOpen className="w-5 h-5 text-emerald-600" />
                        </div>
                        참고 레퍼런스
                    </h3>

                    <div className="bg-emerald-50/50 border border-emerald-100 rounded-2xl p-6">
                        <ul className="space-y-3">
                            {strategy.references.map((ref, idx) => (
                                <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-2 min-w-[6px]"></span>
                                    <span className="leading-relaxed">{ref}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
};

export default StrategyView;
