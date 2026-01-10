
import React, { useState } from 'react';
import { UserPlus, Users, Trash2, Edit3, Briefcase, Code2, Plus, X, Search, Crown, Star } from 'lucide-react';
import { Personnel } from '../../types';

interface PersonnelPanelProps {
  personnelList: Personnel[];
  onAdd: (person: Omit<Personnel, 'id' | 'registeredAt'>) => void;
  onDelete: (id: string) => void;
}

const PersonnelPanel: React.FC<PersonnelPanelProps> = ({ personnelList, onAdd, onDelete }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  // Form State
  const [formData, setFormData] = useState({
    name: '',
    position: '사원',
    role: '',
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
      role: formData.role, // 직위 추가
      experience: formData.experience,
      techStack: formData.techStack
    });
    setFormData({ name: '', position: '사원', role: '', experience: 1, currentTech: '', techStack: [] });
    setIsModalOpen(false);
  };

  const filteredList = personnelList.filter(p =>
    p.name.includes(searchTerm) || p.techStack.some(t => t.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  // 정렬 순서 정의
  const sortedPositions = [...positions].reverse();

  return (
    <div className="h-full flex flex-col">
      {/* Top Header Section */}
      <div className="flex-none mb-6 space-y-4">
        {/* Stats Row */}
        <div className="grid grid-cols-12 gap-4">
          <div className="col-span-12 md:col-span-8 lg:col-span-9">
            <div className="glass-card rounded-[2rem] p-5 shadow-lg shadow-indigo-100/50 border-indigo-50/50 flex flex-wrap items-center justify-between gap-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-indigo-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-200">
                  <Users className="text-white w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Total Personnel</h3>
                  <p className="text-3xl font-black text-slate-900 leading-tight">{personnelList.length} <span className="text-lg text-slate-400 font-bold">명</span></p>
                </div>
              </div>

              <div className="h-10 w-px bg-slate-100 hidden md:block"></div>

              <div className="flex gap-8">
                <div>
                  <span className="text-[9px] font-bold text-indigo-400 uppercase tracking-wider block mb-1">Avg. Exp</span>
                  <p className="text-xl font-black text-indigo-700">
                    {personnelList.length > 0 ? (personnelList.reduce((acc, p) => acc + p.experience, 0) / personnelList.length).toFixed(1) : 0} <span className="text-sm">Yrs</span>
                  </p>
                </div>
                <div>
                  <span className="text-[9px] font-bold text-violet-400 uppercase tracking-wider block mb-1">Skills</span>
                  <p className="text-xl font-black text-violet-700">
                    {Array.from(new Set(personnelList.flatMap(p => p.techStack))).length} <span className="text-sm">Sets</span>
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="col-span-12 md:col-span-4 lg:col-span-3">
            <button
              onClick={() => setIsModalOpen(true)}
              className="w-full h-full glass-card bg-indigo-600 text-white rounded-[2rem] p-5 shadow-xl shadow-indigo-200/50 hover:bg-indigo-700 hover:scale-[1.02] active:scale-95 transition-all flex flex-col items-center justify-center gap-2 group"
            >
              <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center group-hover:rotate-90 transition-transform duration-300">
                <Plus className="w-6 h-6 text-white" />
              </div>
              <span className="font-bold text-lg">신규 인원 등록</span>
            </button>
          </div>
        </div>

        {/* Search Bar Row */}
        <div className="glass-card rounded-2xl p-2 pl-6 pr-2 flex items-center shadow-md shadow-indigo-50/50 border-indigo-50/30">
          <Search className="w-5 h-5 text-slate-400 mr-3" />
          <input
            type="text"
            placeholder="인력 이름, 직위 또는 기술 스택 검색..."
            className="flex-1 bg-transparent border-none focus:outline-none text-sm font-bold text-slate-700 placeholder:text-slate-400 h-10"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
          <div className="text-[10px] font-bold bg-slate-100 text-slate-400 px-3 py-1.5 rounded-xl">
            {filteredList.length} results
          </div>
        </div>
      </div>

      {/* Main Content: Personnel List Grid */}
      <div className="flex-1 overflow-y-auto custom-scrollbar px-2 pb-4 -mx-2">
        {filteredList.length > 0 ? (
          <div className="space-y-12 pb-20">
            {sortedPositions.map(position => {
              const peopleInPosition = filteredList.filter(p => p.position === position);
              if (peopleInPosition.length === 0) return null;

              return (
                <div key={position} className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                  <div className="flex items-center gap-3 mb-5 pl-1 sticky top-0 bg-white/80 backdrop-blur-md z-10 py-2 border-b border-indigo-50/50">
                    <div className="h-4 w-1 bg-indigo-500 rounded-full"></div>
                    <h3 className="text-sm font-black text-indigo-900 flex items-center gap-2">
                      {position}
                      <span className="px-2 py-0.5 bg-indigo-50 text-indigo-600 rounded-full text-[10px] font-bold">
                        {peopleInPosition.length}
                      </span>
                    </h3>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
                    {peopleInPosition.map(person => (
                      <div
                        key={person.id}
                        className="group glass-card bg-white/80 border-slate-100/80 hover:border-indigo-200 hover:shadow-xl hover:shadow-indigo-100/30 p-5 rounded-[1.5rem] transition-all duration-300 flex flex-col relative overflow-hidden h-full min-h-[180px]"
                      >
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-indigo-50 border border-indigo-100 rounded-xl flex items-center justify-center text-indigo-600 font-black text-lg shadow-inner group-hover:bg-indigo-600 group-hover:text-white transition-all duration-300">
                              {person.name.charAt(0)}
                            </div>
                            <div>
                              <h4 className="font-black text-slate-800 text-base tracking-tight group-hover:text-indigo-700 transition-colors flex items-center gap-1.5">
                                {person.name}
                                {person.position === '대표' && <Crown className="w-3 h-3 text-amber-400 fill-amber-400" />}
                              </h4>
                              <div className="flex items-center gap-1.5 mt-0.5">
                                <span className="text-[10px] font-bold text-slate-400">{person.position}</span>
                                {person.role && (
                                  <span className="px-1.5 py-0.5 bg-violet-50 text-violet-600 rounded-md text-[9px] font-bold border border-violet-100/50">
                                    {person.role}
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                          <button
                            onClick={() => onDelete(person.id)}
                            className="text-slate-300 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100 p-1"
                            title="삭제"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>

                        <div className="mb-3">
                          <p className="text-[11px] font-bold text-slate-500 bg-slate-50 inline-flex items-center gap-1 px-2 py-1 rounded-lg">
                            <Briefcase className="w-3 h-3 text-slate-400" />
                            경력 {person.experience}년차
                          </p>
                        </div>

                        {/* Tech Stack Area - pushed to bottom */}
                        <div className="flex-grow"></div>

                        <div className="flex flex-wrap gap-1.5 mt-2">
                          {person.techStack.length > 0 ? person.techStack.slice(0, 4).map(tech => (
                            <span key={tech} className="px-2 py-1 bg-white border border-slate-100 text-slate-600 rounded-lg text-[9px] font-bold group-hover:border-indigo-100 transition-all">
                              {tech}
                            </span>
                          )) : (
                            <span className="text-[9px] text-slate-300 italic">No skills</span>
                          )}
                          {person.techStack.length > 4 && (
                            <span className="px-2 py-1 bg-indigo-50 text-indigo-500 rounded-lg text-[9px] font-bold">
                              +{person.techStack.length - 4}
                            </span>
                          )}
                        </div>

                        {/* Decorative background element */}
                        <div className="absolute -bottom-4 -right-4 w-16 h-16 bg-indigo-500/5 rounded-full group-hover:scale-150 transition-transform duration-500" />
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="h-[60vh] flex flex-col items-center justify-center text-slate-300 bg-slate-50/30 rounded-[3rem] border-2 border-dashed border-slate-100 m-2">
            <div className="w-20 h-20 bg-white rounded-3xl flex items-center justify-center mb-6 shadow-sm border border-slate-50">
              <Users className="w-10 h-10 opacity-20 text-slate-400" />
            </div>
            <p className="font-black text-slate-400 text-lg">등록된 인원이 없습니다.</p>
            <p className="text-sm text-slate-400 mt-2">우측 상단의 버튼을 눌러 인원을 추가하세요.</p>
          </div>
        )}
      </div>

      {/* Registration Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/20 backdrop-blur-sm animate-in fade-in duration-200">
          <div
            className="bg-white rounded-[2.5rem] shadow-2xl shadow-indigo-500/20 w-full max-w-lg overflow-hidden animate-in zoom-in-95 duration-200 border border-white/50"
            onClick={e => e.stopPropagation()}
          >
            <div className="p-8 pb-0 relative">
              <button
                onClick={() => setIsModalOpen(false)}
                className="absolute right-6 top-6 p-2 rounded-full hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
              <h2 className="text-2xl font-black text-slate-900 flex items-center gap-3">
                <div className="w-10 h-10 bg-indigo-100 rounded-xl flex items-center justify-center">
                  <UserPlus className="w-5 h-5 text-indigo-600" />
                </div>
                신규 인원 등록
              </h2>
              <p className="text-slate-500 text-sm font-medium mt-2 pl-1">새로운 회사 구성원의 정보를 입력해주세요.</p>
            </div>

            <div className="p-8">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <label className="text-[10px] font-black text-indigo-400 uppercase tracking-widest ml-1">Full Name</label>
                  <input
                    type="text"
                    placeholder="성함을 입력하세요"
                    className="w-full bg-slate-50 border border-slate-100 rounded-2xl px-5 py-4 text-sm font-bold text-slate-700 focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:bg-white focus:border-indigo-500 transition-all placeholder:text-slate-300"
                    value={formData.name}
                    onChange={e => setFormData({ ...formData, name: e.target.value })}
                    autoFocus
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-indigo-400 uppercase tracking-widest ml-1">Position</label>
                    <div className="relative">
                      <select
                        className="w-full bg-slate-50 border border-slate-100 rounded-2xl px-5 py-4 text-sm font-bold text-slate-700 focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:bg-white focus:border-indigo-500 transition-all appearance-none cursor-pointer"
                        value={formData.position}
                        onChange={e => setFormData({ ...formData, position: e.target.value })}
                      >
                        {positions.map(p => <option key={p} value={p}>{p}</option>)}
                      </select>
                      <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none opacity-40">
                        <Plus className="w-4 h-4 rotate-45" />
                      </div>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-indigo-400 uppercase tracking-widest ml-1">Role (Optional)</label>
                    <input
                      type="text"
                      placeholder="예: 팀장, 파트장"
                      className="w-full bg-slate-50 border border-slate-100 rounded-2xl px-5 py-4 text-sm font-bold text-slate-700 focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:bg-white focus:border-indigo-500 transition-all placeholder:text-slate-300"
                      value={formData.role}
                      onChange={e => setFormData({ ...formData, role: e.target.value })}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-[10px] font-black text-indigo-400 uppercase tracking-widest ml-1">Experience (Years)</label>
                  <input
                    type="number"
                    min="0"
                    className="w-full bg-slate-50 border border-slate-100 rounded-2xl px-5 py-4 text-sm font-bold text-slate-700 focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:bg-white focus:border-indigo-500 transition-all placeholder:text-slate-300"
                    value={formData.experience}
                    onChange={e => setFormData({ ...formData, experience: parseInt(e.target.value) || 0 })}
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-[10px] font-black text-indigo-400 uppercase tracking-widest ml-1">Technology Stack</label>
                  <div className="relative group">
                    <input
                      type="text"
                      placeholder="예: React, Node.js (Enter로 추가)"
                      className="w-full bg-slate-50 border border-slate-100 rounded-2xl px-12 py-4 text-sm font-bold text-slate-700 focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:bg-white focus:border-indigo-500 transition-all placeholder:text-slate-300"
                      value={formData.currentTech}
                      onChange={e => setFormData({ ...formData, currentTech: e.target.value })}
                      onKeyDown={handleAddTech}
                    />
                    <Code2 className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-indigo-300 group-focus-within:text-indigo-500 transition-colors" />
                  </div>
                  <div className="flex flex-wrap gap-2 mt-4 min-h-[48px] p-2 bg-slate-50/50 rounded-2xl border border-slate-100/50">
                    {formData.techStack.length > 0 ? formData.techStack.map(tech => (
                      <span key={tech} className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white text-indigo-600 border border-indigo-100 rounded-xl text-[11px] font-bold shadow-sm animate-in zoom-in-95">
                        {tech}
                        <button type="button" onClick={() => removeTech(tech)} className="hover:text-red-500 transition-colors">
                          <X className="w-3 h-3" />
                        </button>
                      </span>
                    )) : (
                      <span className="text-xs font-bold text-slate-300 italic flex items-center justify-center w-full h-full">기술 스택을 등록해주세요</span>
                    )}
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full group/btn relative overflow-hidden bg-indigo-600 text-white font-bold py-4 rounded-2xl transition-all hover:bg-indigo-700 hover:shadow-xl hover:shadow-indigo-200/50 active:scale-[0.98] flex items-center justify-center gap-2 mt-4"
                >
                  <Plus className="w-5 h-5 transition-transform group-hover/btn:rotate-90" />
                  신규 인원 등록 완료
                </button>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PersonnelPanel;
