import React from 'react';
import { StrategyConfig } from '../../types';
import { Target, BookOpen, Lightbulb } from 'lucide-react';

interface StrategyViewProps {
    strategy: StrategyConfig;
}

const StrategyView: React.FC<StrategyViewProps> = ({ strategy }) => {
    return (
        <div className="space-y-8 animate-in slide-in-from-bottom duration-500">

            {/* 1. Winning Strategy */}
            <div>
                <h3 className="text-lg font-bold text-indigo-900 mb-4 flex items-center gap-2">
                    <div className="bg-indigo-100 p-1.5 rounded-lg">
                        <Target className="w-5 h-5 text-indigo-600" />
                    </div>
                    수주 확보 전략
                </h3>

                <div className="grid gap-4">
                    {strategy.win_strategy.map((item, idx) => (
                        <div key={idx} className="bg-white border border-indigo-100 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-indigo-200 transition-all group relative overflow-hidden">
                            <div className="absolute top-0 left-0 w-1 h-full bg-indigo-500"></div>
                            <span className="absolute top-4 right-4 text-xs font-black text-indigo-100 text-[40px] leading-none -z-0 opacity-50 select-none group-hover:opacity-100 transition-opacity">
                                {idx + 1}
                            </span>
                            <p className="text-gray-700 font-medium leading-relaxed relative z-10 group-hover:text-indigo-900 transition-colors">
                                {item}
                            </p>
                        </div>
                    ))}
                </div>
            </div>

            {/* 2. References (If any) */}
            {strategy.references && strategy.references.length > 0 && (
                <div>
                    <h3 className="text-lg font-bold text-emerald-900 mb-4 flex items-center gap-2 mt-8">
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
