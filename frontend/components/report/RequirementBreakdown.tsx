import React, { useState } from 'react';
import { ChevronDown, ChevronRight, CheckSquare, Layers } from 'lucide-react';

interface RequirementBreakdownProps {
    requirements: Record<string, string[]>;
}

const RequirementBreakdown: React.FC<RequirementBreakdownProps> = ({ requirements }) => {
    const categories = Object.keys(requirements);
    const [openCategory, setOpenCategory] = useState<string | null>(categories[0] || null);

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
                    총 {categories.length}개 카테고리 / {Object.values(requirements).flat().length}개 세부항목
                </p>
                <button
                    onClick={() => setOpenCategory(null)}
                    className="text-xs text-indigo-500 hover:text-indigo-700 font-medium cursor-pointer"
                >
                    모두 접기
                </button>
            </div>

            {categories.map((category) => (
                <div key={category} className="border border-gray-200 rounded-xl bg-white overflow-hidden shadow-sm hover:shadow-md transition-all duration-200">
                    <button
                        onClick={() => toggleCategory(category)}
                        className={`w-full flex items-center justify-between p-4 text-left transition-colors ${openCategory === category ? 'bg-indigo-50/50' : 'hover:bg-gray-50'}`}
                    >
                        <div className="flex items-center gap-3">
                            <div className={`p-1.5 rounded-lg ${openCategory === category ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-500'}`}>
                                <Layers className="w-4 h-4" />
                            </div>
                            <h4 className={`font-bold text-sm ${openCategory === category ? 'text-indigo-900' : 'text-gray-700'}`}>
                                {category}
                            </h4>
                            <span className="text-xs bg-gray-100 text-gray-500 py-0.5 px-2 rounded-full font-medium">
                                {requirements[category].length}
                            </span>
                        </div>
                        {openCategory === category ? (
                            <ChevronDown className="w-4 h-4 text-indigo-400" />
                        ) : (
                            <ChevronRight className="w-4 h-4 text-gray-400" />
                        )}
                    </button>

                    {/* Expanded Content with Animation */}
                    <div
                        className={`overflow-hidden transition-all duration-300 ease-in-out ${openCategory === category ? 'max-h-[1000px] opacity-100' : 'max-h-0 opacity-0'}`}
                    >
                        <div className="p-4 pt-0 bg-indigo-50/10 border-t border-indigo-50">
                            <ul className="space-y-2 mt-3">
                                {requirements[category].map((req, idx) => (
                                    <li key={idx} className="flex items-start gap-3 text-sm text-gray-600 pl-2 group">
                                        <CheckSquare className="w-4 h-4 min-w-[16px] mt-0.5 text-indigo-300 group-hover:text-indigo-500 transition-colors" />
                                        <span className="leading-relaxed group-hover:text-gray-900 transition-colors">{req}</span>
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
