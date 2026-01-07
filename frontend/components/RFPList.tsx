import React from 'react';
import { RFP } from '../types';
import { Search, FileText, Calendar, ChevronRight, Trash2, ChevronLeft } from 'lucide-react';

interface RFPListProps {
  rfps: RFP[];
  onSelectRFP: (rfp: RFP) => void;
  selectedRFPId?: string;
  onDelete?: (id: string, e: React.MouseEvent) => void;
}

const RFPList: React.FC<RFPListProps> = ({ rfps, onSelectRFP, selectedRFPId, onDelete }) => {
  const [searchTerm, setSearchTerm] = React.useState('');
  const [page, setPage] = React.useState(1);
  const itemsPerPage = 8;

  const filteredRFPs = rfps.filter(rfp =>
    rfp.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const totalPages = Math.ceil(filteredRFPs.length / itemsPerPage);
  const currentItems = filteredRFPs.slice(
    (page - 1) * itemsPerPage,
    page * itemsPerPage
  );

  // Reset page when search changes
  React.useEffect(() => {
    setPage(1);
  }, [searchTerm]);

  if (rfps.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-gray-400 p-8 glass-card border-indigo-50/50">
        <div className="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mb-4 inner-shadow">
          <FileText className="w-8 h-8 opacity-20" />
        </div>
        <p className="text-sm font-medium">등록된 제안서가 없습니다</p>
        <p className="text-xs mt-1 opacity-70">새 제안서를 업로드하거나 API를 통해 가져오세요</p>
      </div>
    );
  }

  return (
    <div className="glass-card rounded-3xl shadow-xl shadow-indigo-100/50 flex flex-col h-full overflow-hidden transition-all border-indigo-50/50">
      {/* Search Header */}
      <div className="p-5 border-b border-gray-100/50 bg-white/40">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-bold text-gray-800">제안서 목록</h2>
          <span className="text-[10px] font-bold px-2 py-0.5 bg-indigo-50 text-indigo-600 rounded-full">
            TOTAL {filteredRFPs.length}
          </span>
        </div>
        <div className="relative group">
          <input
            type="text"
            placeholder="제안서 검색..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-white/80 border border-gray-100 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 transition-all text-gray-700 placeholder-gray-400 shadow-sm group-hover:shadow-md"
          />
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 group-hover:text-indigo-500 transition-colors" />
        </div>
      </div>

      {/* List Content */}
      <div className="flex-1 overflow-y-auto custom-scrollbar p-3 space-y-2 bg-white/30">
        {currentItems.map((rfp) => (
          <div
            key={rfp.id}
            onClick={() => onSelectRFP(rfp)}
            className={`group relative p-4 rounded-2xl border transition-all cursor-pointer hover:shadow-lg hover:shadow-indigo-100/50 hover:-translate-y-0.5 ${selectedRFPId === rfp.id
                ? 'bg-white border-indigo-500 ring-1 ring-indigo-500 shadow-md shadow-indigo-100'
                : 'bg-white/60 border-transparent hover:border-indigo-100'
              }`}
          >
            {/* Status Indicator Bar */}
            <div className={`absolute left-0 top-4 bottom-4 w-1 rounded-r-full transition-colors ${rfp.status === 'completed' ? 'bg-emerald-400' :
                rfp.status === 'error' ? 'bg-red-400' : 'bg-amber-400'
              }`}></div>

            <div className="pl-3 pr-8">
              {/* Header: Date & Status */}
              <div className="flex items-center justify-between mb-1.5">
                <span className="flex items-center gap-1.5 text-[10px] font-bold text-gray-400 bg-gray-50 px-1.5 py-0.5 rounded-md">
                  <Calendar className="w-3 h-3" />
                  {rfp.analysisDate}
                </span>
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded-full border ${rfp.status === 'completed' ? 'bg-emerald-50 text-emerald-600 border-emerald-100' :
                      rfp.status === 'error' ? 'bg-red-50 text-red-600 border-red-100' : 'bg-amber-50 text-amber-600 border-amber-100'
                    }`}>
                    {rfp.status === 'completed' ? '분석완료' : rfp.status === 'error' ? '오류' : '분석중'}
                  </span>
                </div>
              </div>

              {/* Title */}
              <h3 className={`text-sm font-bold leading-snug line-clamp-2 mb-1.5 ${selectedRFPId === rfp.id ? 'text-indigo-900 initial' : 'text-gray-700'}`}>
                {rfp.title}
              </h3>

              {/* Footer: Summary Preview */}
              <p className="text-[11px] text-gray-400 line-clamp-1">
                {rfp.summary ? rfp.summary.replace(/\n/g, ' ') : '요약 정보 없음'}
              </p>
            </div>

            {/* Arrow Icon */}
            <ChevronRight className={`absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 transition-all ${selectedRFPId === rfp.id ? 'text-indigo-500 translate-x-1' : 'text-gray-300 opacity-0 group-hover:opacity-100'
              }`} />

            {/* Delete Button (Visible on Hover / Active) */}
            {onDelete && (
              <button
                onClick={(e) => onDelete(rfp.id, e)}
                className="absolute right-2 top-2 p-1.5 rounded-lg text-gray-300 hover:text-red-500 hover:bg-red-50 transition-all opacity-0 group-hover:opacity-100 z-10"
                title="제안서 삭제"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}

          </div>
        ))}

        {currentItems.length === 0 && (
          <div className="p-8 text-center text-gray-400 text-xs">
            검색 결과가 없습니다.
          </div>
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="p-3 border-t border-gray-100/50 bg-white/40 flex justify-center gap-1">
          <button
            disabled={page === 1}
            onClick={() => setPage(p => Math.max(1, p - 1))}
            className="w-7 h-7 flex items-center justify-center rounded-lg border border-gray-200 hover:bg-white disabled:opacity-30 transition-all"
          >
            <ChevronLeft className="w-3 h-3 text-gray-500" />
          </button>
          <span className="text-xs font-medium text-gray-500 flex items-center px-2">
            {page} / {totalPages}
          </span>
          <button
            disabled={page === totalPages}
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            className="w-7 h-7 flex items-center justify-center rounded-lg border border-gray-200 hover:bg-white disabled:opacity-30 transition-all"
          >
            <ChevronRight className="w-3 h-3 text-gray-500" />
          </button>
        </div>
      )}
    </div>
  );
};

export default RFPList;
