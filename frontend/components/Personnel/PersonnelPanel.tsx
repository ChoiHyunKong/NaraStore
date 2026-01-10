
import React, { useState } from 'react';
import { UserPlus, Users, Trash2, Code2, Plus, X, Search, Briefcase, Crown } from 'lucide-react';
import { Personnel } from '../../types';

interface PersonnelPanelProps {
  personnelList: Personnel[];
  onAdd: (person: Omit<Personnel, 'id' | 'registeredAt'>) => void;
  onDelete: (id: string) => void;
}

const PersonnelPanel: React.FC<PersonnelPanelProps> = ({ personnelList, onAdd, onDelete }) => {
  const [searchTerm, setSearchTerm] = useState('');

  // Form State
  const [formData, setFormData] = useState({
    name: '',
    position: '사원',
    experience: 1,
    currentTech: '',
    techStack: [] as string[]
  });

  const positions = ['사원', '대리', '과장', '차장', '부장', '이사', '대표'];

  const handleAddTech = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && formData.currentTech.trim()) {
      e.preventDefault();
      if (!formData.techStack.includes(formData.currentTech.trim())) {
        setFormData({
          ...formData,
          techStack: [...formData.techStack, formData.currentTech.trim()],
          currentTech: ''
        });
      }
    }
  };

  const removeTech = (tech: string) => {
    setFormData({
      ...formData,
      techStack: formData.techStack.filter(t => t !== tech)
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name) return;
    onAdd({
      name: formData.name,
      position: formData.position,
      experience: formData.experience,
      techStack: formData.techStack
    });
    setFormData({ name: '', position: '사원', experience: 1, currentTech: '', techStack: [] });
  };

  const filteredList = personnelList.filter(p =>
    p.name.includes(searchTerm) || p.techStack.some(t => t.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="grid grid-cols-12 gap-6 h-full">
      {/* Left Column: Stats & Registration Form (Reduced width: col-span-3) */}
      <div className="col-span-12 lg:col-span-3 space-y-4 h-full flex flex-col">
        {/* Stats Card */}
        <div className="glass-card rounded-[2rem] p-5 shadow-xl shadow-indigo-100/50 border-indigo-50/50 flex-shrink-0">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-200">
              <Users className="text-white w-5 h-5" />
            </div>
            <div>
              <h3 className="text-[9px] font-black text-slate-400 uppercase tracking-[0.2em]">Overview</h3>
              <p className="text-2xl font-black text-slate-900 leading-tight">{personnelList.length} 명</p>
            </div>
          </div>
          <div className="space-y-3">
            <div className="bg-indigo-50/50 p-3 rounded-xl border border-indigo-100/20 flex justify-between items-center">
              <span className="text-[9px] font-bold text-indigo-400 uppercase tracking-wider">Avg. Exp</span>
              <p className="text-base font-black text-indigo-700">
                {personnelList.length > 0 ? (personnelList.reduce((acc, p) => acc + p.experience, 0) / personnelList.length).toFixed(1) : 0} <span className="text-[10px] text-indigo-400">Yrs</span>
              </p>
            </div>
            <div className="bg-violet-50/50 p-3 rounded-xl border border-violet-100/20 flex justify-between items-center">
              <span className="text-[9px] font-bold text-violet-400 uppercase tracking-wider">Skills</span>
              <p className="text-base font-black text-violet-700">
                {Array.from(new Set(personnelList.flatMap(p => p.techStack))).length} <span className="text-[10px] text-violet-400">Sets</span>
              </p>
            </div>
          </div>
        </div>

        {/* Registration Form Card (Scrollable if needed) */}
        <div className="glass-card rounded-[2rem] p-6 shadow-xl shadow-indigo-100/50 border-indigo-50/50 relative overflow-hidden flex-1 overflow-y-auto custom-scrollbar">
          <div className="flex items-center gap-2 mb-6">
            <UserPlus className="w-5 h-5 text-indigo-600" />
            <h2 className="text-lg font-bold text-slate-900">인원 등록</h2>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-1.5">
              <label className="text-[9px] font-black text-indigo-300 uppercase tracking-widest ml-1">Name</label>
              <input
                type="text"
                placeholder="성함 입력"
                className="w-full bg-indigo-50/30 border border-transparent rounded-xl px-4 py-3 text-sm font-bold text-indigo-900 focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:bg-white focus:border-indigo-400 transition-all placeholder:text-indigo-200"
                value={formData.name}
                onChange={e => setFormData({ ...formData, name: e.target.value })}
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-[9px] font-black text-indigo-300 uppercase tracking-widest ml-1">Position</label>
              <div className="relative">
                <select
                  className="w-full bg-indigo-50/30 border border-transparent rounded-xl px-4 py-3 text-sm font-bold text-indigo-900 focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:bg-white focus:border-indigo-400 transition-all appearance-none cursor-pointer"
                  value={formData.position}
                  onChange={e => setFormData({ ...formData, position: e.target.value })}
                >
                  {positions.map(p => <option key={p} value={p}>{p}</option>)}
                </select>
                <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none opacity-40">
                  <Plus className="w-3.5 h-3.5 rotate-45" />
                </div>
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-[9px] font-black text-indigo-300 uppercase tracking-widest ml-1">Exp. (Yrs)</label>
              <input
                type="number"
                min="0"
                className="w-full bg-indigo-50/30 border border-transparent rounded-xl px-4 py-3 text-sm font-bold text-indigo-900 focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:bg-white focus:border-indigo-400 transition-all"
                value={formData.experience}
                onChange={e => setFormData({ ...formData, experience: parseInt(e.target.value) || 0 })}
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-[9px] font-black text-indigo-300 uppercase tracking-widest ml-1">Tech Stack</label>
              <div className="relative group">
                <input
                  type="text"
                  placeholder="기술 스택 (Enter)"
                  className="w-full bg-indigo-50/30 border border-transparent rounded-xl px-10 py-3 text-sm font-bold text-indigo-900 focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:bg-white focus:border-indigo-400 transition-all placeholder:text-indigo-200"
                  value={formData.currentTech}
                  onChange={e => setFormData({ ...formData, currentTech: e.target.value })}
                  onKeyDown={handleAddTech}
                />
                <Code2 className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-indigo-300 group-focus-within:text-indigo-500 transition-colors" />
              </div>
              <div className="flex flex-wrap gap-1.5 mt-2 min-h-[30px]">
                {formData.techStack.map(tech => (
                  <span key={tech} className="inline-flex items-center gap-1 px-2 py-1 bg-indigo-100/50 text-indigo-600 border border-indigo-200/50 rounded-lg text-[10px] font-black uppercase tracking-wider animate-in zoom-in-95">
                    {tech}
                    <button type="button" onClick={() => removeTech(tech)} className="hover:text-red-500 transition-colors">
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            </div>

            <button
              type="submit"
              className="w-full group/btn bg-indigo-600 text-white font-bold py-3.5 rounded-xl transition-all hover:bg-indigo-700 hover:shadow-lg hover:shadow-indigo-200/50 active:scale-[0.98] flex items-center justify-center gap-2 mt-4"
            >
              <Plus className="w-4 h-4 transition-transform group-hover/btn:rotate-90" />
              신규 등록
            </button>
          </form>
        </div>
      </div>

      {/* Right Column: Personnel List Grid (Expanded width: col-span-9) */}
      <div className="col-span-12 lg:col-span-9 h-full flex flex-col">
        <div className="glass-card rounded-[2.5rem] shadow-xl shadow-indigo-100/50 border-indigo-50/50 flex flex-col h-full overflow-hidden">
          {/* Header */}
          <div className="p-8 pb-4 flex-none">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-2">
              <h2 className="text-xl font-black text-slate-900 flex items-center gap-3">
                <Users className="w-6 h-6 text-indigo-600" />
                회사 인원 현황
              </h2>
              <div className="relative w-full md:w-80 group">
                <input
                  type="text"
                  placeholder="이름 또는 기술 스택 검색..."
                  className="w-full bg-slate-50/50 border border-slate-100 rounded-2xl py-3.5 pl-12 pr-4 text-xs font-bold focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:bg-white focus:border-indigo-400 transition-all"
                  value={searchTerm}
                  onChange={e => setSearchTerm(e.target.value)}
                />
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-300 group-focus-within:text-indigo-400 transition-colors" />
              </div>
            </div>
          </div>

          {/* Scrollable Content Area */}
          <div className="flex-1 overflow-y-auto custom-scrollbar px-8 pb-8">
            {filteredList.length > 0 ? (
              <div className="space-y-8">
                {[...positions].reverse().map(position => {
                  const peopleInPosition = filteredList.filter(p => p.position === position);
                  if (peopleInPosition.length === 0) return null;

                  return (
                    <div key={position} className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                      <div className="flex items-center gap-3 mb-4 pl-1 sticky top-0 bg-white/90 backdrop-blur-sm z-10 py-2">
                        <div className="h-4 w-1 bg-indigo-500 rounded-full"></div>
                        <h3 className="text-sm font-black text-indigo-900 flex items-center gap-2">
                          {position}
                          <span className="px-2 py-0.5 bg-indigo-50 text-indigo-600 rounded-full text-[10px] font-bold">
                            {peopleInPosition.length}
                          </span>
                        </h3>
                        <div className="h-px flex-1 bg-indigo-50"></div>
                      </div>

                      {/* Grid Layout: Up to 4 columns */}
                      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-4 auto-rows-fr">
                        {peopleInPosition.map(person => (
                          <div
                            key={person.id}
                            className="group glass-card bg-white/80 border-slate-100/80 hover:border-indigo-200 hover:shadow-2xl hover:shadow-indigo-100/30 p-5 rounded-[2rem] transition-all duration-300 flex flex-col relative overflow-hidden"
                          >
                            <div className="flex items-start justify-between mb-4">
                              <div className="flex items-center gap-3">
                                <div className="w-12 h-12 bg-indigo-50 border border-indigo-100 rounded-2xl flex items-center justify-center text-indigo-600 font-black text-lg shadow-inner group-hover:bg-indigo-600 group-hover:text-white transition-all duration-500">
                                  {person.name.charAt(0)}
                                </div>
                                <div>
                                  <div className="flex items-center gap-2">
                                    <h4 className="font-black text-slate-900 text-base tracking-tight group-hover:text-indigo-700 transition-colors">
                                      {person.name}
                                      {person.position === '대표' && <Crown className="inline-block w-3 h-3 text-amber-400 fill-amber-400 ml-1" />}
                                    </h4>
                                    <span className="px-2 py-0.5 bg-indigo-600 text-white rounded-lg text-[9px] font-black shadow-md shadow-indigo-100">{person.position}</span>
                                  </div>
                                  <p className="text-[11px] font-bold text-slate-400 mt-1 flex items-center gap-1">
                                    <Briefcase className="w-3 h-3 text-indigo-300" />
                                    경력 {person.experience}년차
                                  </p>
                                </div>
                              </div>
                              <button
                                onClick={() => onDelete(person.id)}
                                className="p-2 text-slate-200 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all opacity-0 group-hover:opacity-100"
                                title="삭제"
                              >
                                <Trash2 className="w-3.5 h-3.5" />
                              </button>
                            </div>

                            {/* Tech Stack Area - pushed to bottom */}
                            <div className="flex-grow"></div>

                            <div className="space-y-2 mt-4">
                              <div className="flex items-center gap-1.5">
                                <Code2 className="w-3 h-3 text-indigo-400" />
                                <span className="text-[9px] font-black text-indigo-300 uppercase tracking-widest">Stacks</span>
                              </div>
                              <div className="flex flex-wrap gap-1.5">
                                {person.techStack.length > 0 ? person.techStack.slice(0, 5).map(tech => (
                                  <span key={tech} className="px-2 py-1 bg-slate-50 text-slate-600 rounded-lg text-[10px] font-bold border border-slate-100 group-hover:border-indigo-100 group-hover:bg-indigo-50/30 transition-all">
                                    {tech}
                                  </span>
                                )) : (
                                  <span className="text-[10px] text-slate-300 italic">등록된 기술 없음</span>
                                )}
                                {person.techStack.length > 5 && (
                                  <span className="px-2 py-1 bg-slate-50 text-slate-400 rounded-lg text-[10px] font-bold border border-slate-100">+{person.techStack.length - 5}</span>
                                )}
                              </div>
                            </div>

                            {/* Decorative background element */}
                            <div className="absolute -bottom-6 -right-6 w-20 h-20 bg-indigo-500/5 rounded-full group-hover:scale-150 transition-transform duration-700" />
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-slate-300 bg-slate-50/30 rounded-[3rem] border-2 border-dashed border-slate-100 min-h-[300px]">
                <div className="w-16 h-16 bg-slate-100 rounded-3xl flex items-center justify-center mb-4">
                  <Users className="w-8 h-8 opacity-20" />
                </div>
                <p className="font-black text-slate-400">등록된 인원이 없거나 검색 결과가 없습니다.</p>
                <p className="text-xs text-slate-300 mt-1">좌측 폼을 이용해 새로운 인력을 추가하세요.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PersonnelPanel;
