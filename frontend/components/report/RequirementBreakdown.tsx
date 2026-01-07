import React, { useState } from 'react';
import { ChevronDown, ChevronRight, CheckSquare, Layers } from 'lucide-react';

import { RequirementCategory } from '../../types';

interface RequirementBreakdownProps {
    requirements: RequirementCategory[];
}

const RequirementBreakdown: React.FC<RequirementBreakdownProps> = ({ requirements }) => {
    const categories = requirements;
    const [openCategory, setOpenCategory] = useState<string | null>(categories[0]?.category || null);

    const toggleCategory = (category: string) => {
        setOpenCategory(prev => prev === category ? null : category);
    };

    if (categories.length === 0) {
        return (
            <div className="p-8 text-center text-gray-500 bg-gray-50 rounded-2xl border border-gray-100">
                <Layers className="w-10 h-10 mx-auto mb-3 opacity-20" />
                <p>추출된 요구사항이 없습니다.</p>
            </div>
        );
    }

    return (
        <div className="space-y-4 animate-in slide-in-from-bottom duration-500">
            <div className="flex items-center justify-between mb-2">
                <p className="text-sm font-bold text-gray-600">
                    총 {categories.length}개 카테고리 / {categories.reduce((acc, cat) => acc + cat.items.length, 0)}개 세부항목
                </p>
                <button
                    onClick={() => setOpenCategory(null)}
                    className="text-xs text-indigo-500 hover:text-indigo-700 font-medium cursor-pointer"
                >
                    모두 접기
                </button>
            </div>

            {categories.map((reqCategory) => (
                <div key={reqCategory.category} className="border border-gray-200 rounded-xl bg-white overflow-hidden shadow-sm hover:shadow-md transition-all duration-200">
                    <button
                        onClick={() => toggleCategory(reqCategory.category)}
                        className={`w-full flex items-center justify-between p-4 text-left transition-colors ${openCategory === reqCategory.category ? 'bg-indigo-50/50' : 'hover:bg-gray-50'}`}
                    >
                        <div className="flex items-center gap-3">
                            <div className={`p-1.5 rounded-lg ${openCategory === reqCategory.category ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-500'}`}>
                                <Layers className="w-4 h-4" />
                            </div>
                            <h4 className={`font-bold text-sm ${openCategory === reqCategory.category ? 'text-indigo-900' : 'text-gray-700'}`}>
                                {reqCategory.category}
                            </h4>
                            <span className="text-xs bg-gray-100 text-gray-500 py-0.5 px-2 rounded-full font-medium">
                                {reqCategory.items.length}
                            </span>
                        </div>
                        {openCategory === reqCategory.category ? (
                            <ChevronDown className="w-4 h-4 text-indigo-400" />
                        ) : (
                            <ChevronRight className="w-4 h-4 text-gray-400" />
                        )}
                    </button>

                    {/* Expanded Content with Animation */}
                    <div
                        className={`overflow-hidden transition-all duration-300 ease-in-out ${openCategory === reqCategory.category ? 'max-h-[1000px] opacity-100' : 'max-h-0 opacity-0'}`}
                    >
                        <div className="p-4 pt-0 bg-indigo-50/10 border-t border-indigo-50">
                            <ul className="space-y-2 mt-3">
                                {reqCategory.items.map((item, idx) => (
                                    <li key={idx} className="flex items-start gap-3 text-sm text-gray-600 pl-2 group">
                                        <CheckSquare className="w-4 h-4 min-w-[16px] mt-0.5 text-indigo-300 group-hover:text-indigo-500 transition-colors" />
                                        <span className="leading-relaxed group-hover:text-gray-900 transition-colors">{item}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default RequirementBreakdown;
