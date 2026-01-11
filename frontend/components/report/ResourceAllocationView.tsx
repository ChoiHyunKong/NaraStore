import React, { useState, useEffect } from 'react';
import { Users, UserPlus, CheckCircle2, AlertCircle, Briefcase, Award } from 'lucide-react';
import { AnalysisResultData, Personnel, ResourceRequirement } from '../../types';

interface ResourceAllocationViewProps {
    data: AnalysisResultData;
    personnelList: Personnel[];
}

interface MatchedPersonnel extends Personnel {
    matchScore: number;
    matchedSkills: string[];
}

const ResourceAllocationView: React.FC<ResourceAllocationViewProps> = ({ data, personnelList }) => {
    const requirements = data.resource_requirements || [];

    // State for drag and drop or manual assignment (simplified for now)
    const [assignedTeam, setAssignedTeam] = useState<Record<string, Personnel[]>>({});

    // Auto-matching logic
    const getRecommendedPersonnel = (req: ResourceRequirement): MatchedPersonnel[] => {
        return personnelList
            .map(person => {
                const matchedSkills = req.required_skills.filter(skill =>
                    person.techStack.some(pSkill => pSkill.toLowerCase().includes(skill.toLowerCase()))
                );

                let score = 0;
                // Skill Match (50%)
                if (req.required_skills.length > 0) {
                    score += (matchedSkills.length / req.required_skills.length) * 50;
                }

                // Role Match (20%) - Simple keyword matching
                if (person.role && req.role.includes(person.role)) score += 20;
                if (person.position && req.role.includes(person.position)) score += 10;

                // Experience (30%) - Assume senior roles need more exp
                if (req.role.includes('PM') || req.role.includes('PL') || req.role.includes('고급')) {
                    if (person.experience >= 10) score += 30;
                    else if (person.experience >= 5) score += 15;
                } else {
                    score += 10; // Junior roles
                }

                return { ...person, matchScore: score, matchedSkills };
            })
            .filter(p => p.matchScore > 0)
            .sort((a, b) => b.matchScore - a.matchScore);
    };

    return (
        <div className="space-y-8 animate-fadeIn">
            <div className="flex items-center gap-3 mb-2">
                <div className="bg-indigo-600 rounded-xl p-2 shadow-lg shadow-indigo-200">
                    <Users className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h2 className="text-2xl font-bold text-slate-900">인력 배분 제안</h2>
                    <p className="text-gray-500">AI 분석 기반 최적의 팀 구성을 제안합니다.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Left: Resource Requirements (Demand) */}
                <div className="space-y-6">
                    <h3 className="text-lg font-bold text-indigo-900 flex items-center gap-2">
                        <AlertCircle className="w-5 h-5" /> 필요 인력 요건 (AI 분석)
                    </h3>

                    {requirements.length === 0 ? (
                        <div className="p-8 text-center text-gray-400 bg-gray-50 rounded-xl border border-gray-100">
                            분석된 인력 요건이 없습니다.
                        </div>
                    ) : (
                        requirements.map((req, idx) => {
                            const recommended = getRecommendedPersonnel(req);
                            return (
                                <div key={idx} className="bg-white border-2 border-indigo-50 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all">
                                    <div className="flex justify-between items-start mb-4">
                                        <div>
                                            <h4 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                                                {req.role}
                                                <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full">{req.count}명</span>
                                            </h4>
                                            <p className="text-sm text-gray-500 mt-1">{req.reason}</p>
                                        </div>
                                    </div>

                                    <div className="space-y-3">
                                        <div className="flex flex-wrap gap-2">
                                            {req.required_skills.map((skill, i) => (
                                                <span key={i} className="text-xs font-medium text-slate-600 bg-slate-100 px-2 py-1 rounded-md border border-slate-200">
                                                    {skill}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Recommendation Preview */}
                                    <div className="mt-5 pt-4 border-t border-gray-100">
                                        <p className="text-xs font-bold text-slate-400 mb-2 uppercase tracking-wider">추천 인재 (Top Match)</p>
                                        <div className="space-y-2">
                                            {recommended.slice(0, 3).map(person => (
                                                <div key={person.id} className="flex items-center justify-between bg-indigo-50/50 p-2 rounded-lg border border-indigo-100/50">
                                                    <div className="flex items-center gap-3">
                                                        <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center text-indigo-600 font-bold text-xs shadow-sm border border-indigo-100">
                                                            {person.name[0]}
                                                        </div>
                                                        <div>
                                                            <p className="text-sm font-bold text-slate-800">{person.name} <span className="text-xs font-normal text-gray-500">{person.position}</span></p>
                                                            <p className="text-[10px] text-indigo-500">
                                                                매칭률 {person.matchScore.toFixed(0)}% • {person.matchedSkills.join(', ')}
                                                            </p>
                                                        </div>
                                                    </div>
                                                    {person.status === 'busy' && (
                                                        <span className="text-[10px] text-amber-600 bg-amber-50 px-2 py-1 rounded-full border border-amber-100">투입중</span>
                                                    )}
                                                    {(!person.status || person.status === 'available') && (
                                                        <div className="text-green-500">
                                                            <CheckCircle2 className="w-4 h-4" />
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                            {recommended.length === 0 && (
                                                <p className="text-sm text-gray-400 italic">적합한 내부 인력을 찾지 못했습니다.</p>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            );
                        })
                    )}
                </div>

                {/* Right: Personnel Pool Status (Supply) */}
                <div className="space-y-6">
                    <h3 className="text-lg font-bold text-slate-700 flex items-center gap-2">
                        <Briefcase className="w-5 h-5" /> 현재 가용 인력 현황
                    </h3>

                    <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-200 h-full overflow-y-auto" style={{ maxHeight: '800px' }}>
                        <div className="space-y-4">
                            {personnelList.length === 0 ? (
                                <p className="text-center text-gray-400 py-10">등록된 인력이 없습니다. 인원 관리 메뉴에서 등록해주세요.</p>
                            ) : (
                                personnelList.map(person => (
                                    <div key={person.id} className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-xl transition-colors border border-transparent hover:border-gray-100">
                                        <div className="flex items-center gap-3">
                                            <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm text-white shadow-md ${person.status === 'busy' ? 'bg-gray-400' : 'bg-gradient-to-br from-indigo-500 to-purple-500'}`}>
                                                {person.name[0]}
                                            </div>
                                            <div>
                                                <h5 className="font-bold text-slate-800">{person.name}</h5>
                                                <p className="text-xs text-gray-500">{person.position} • {person.experience}년차</p>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <span className={`text-xs px-2 py-1 rounded-full font-medium ${person.status === 'busy' ? 'bg-gray-100 text-gray-500' : 'bg-green-100 text-green-600'}`}>
                                                {person.status === 'busy' ? '진행중' : '가용가능'}
                                            </span>
                                            <div className="mt-1 flex gap-1 justify-end">
                                                {person.techStack.slice(0, 2).map((t, i) => (
                                                    <span key={i} className="text-[10px] text-slate-400 bg-slate-50 px-1 rounded border border-slate-100">{t}</span>
                                                ))}
                                                {person.techStack.length > 2 && <span className="text-[10px] text-slate-400">+</span>}
                                            </div>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResourceAllocationView;
