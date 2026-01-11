import React, { useRef, useState } from 'react';
import { FileText, Upload, Loader2, Download, SearchCode, AlertCircle, CheckCircle2 } from 'lucide-react';
import ResourceAllocationView from './report/ResourceAllocationView';
import SummaryCard from './report/SummaryCard';
import RequirementBreakdown from './report/RequirementBreakdown';
import StrategyView from './report/StrategyView';
import { Personnel, RFP, TabType } from '../types';

interface AnalysisPanelProps {
  currentRFP: RFP | null;
  onUpload: (file: File) => void;
  isAnalyzing: boolean;
  apiKeySet?: boolean;
  personnelList?: Personnel[];
}

const AnalysisPanel: React.FC<AnalysisPanelProps> = ({ currentRFP, onUpload, isAnalyzing, apiKeySet = false, personnelList = [] }) => {
  const [activeTab, setActiveTab] = useState<TabType>('summary');
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // ...
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  const triggerUpload = () => fileInputRef.current?.click();

  const handleDownloadPDF = async () => {
    // ... (PDF logic same)
    if (!currentRFP) return;
    // ...
    if (!currentRFP.structuredAnalysis) {
      alert('구조화된 분석 데이터가 없어 전체 리포트를 생성할 수 없습니다. (이전 버전 데이터)');
      return;
    }

    try {
      setIsGeneratingPdf(true);
      const response = await fetch('http://localhost:8000/api/report/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          analysis_data: currentRFP.structuredAnalysis
        }),
      });

      if (!response.ok) throw new Error('PDF generation failed');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${currentRFP.title}_분석리포트.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

    } catch (error) {
      console.error('PDF Download Error:', error);
      alert('PDF 생성 중 오류가 발생했습니다. (백엔드 연결 확인 필요)');
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  return (
    <div className="glass-card rounded-3xl shadow-xl shadow-indigo-100/50 flex flex-col flex-1 h-full min-h-0 overflow-hidden transition-all border-indigo-50/50 relative">
      <div className="flex-none p-6 md:p-8">
        <h2 className="text-xl font-bold mb-4 text-gray-800 flex items-center gap-2">
          <FileText className="w-5 h-5 text-indigo-600" />
          RFP 정밀 분석
        </h2>


        <div
          onClick={triggerUpload}
          className="relative overflow-hidden group bg-gradient-to-br from-indigo-50/50 to-violet-50/50 border-2 border-dashed border-indigo-200 rounded-2xl py-4 px-6 flex flex-col items-center justify-center cursor-pointer hover:border-indigo-400 transition-all"
        >
          <div className="absolute top-0 left-0 w-full h-1 bg-indigo-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-500"></div>
          <Upload className="w-5 h-5 text-indigo-500 mb-2 group-hover:scale-110 transition-transform" />
          <div className="text-center">
            <p className="text-xs text-indigo-900 font-bold">제안서 업로드 (PDF, HWP, PPTX)</p>
          </div>
          <input
            type="file"
            ref={fileInputRef}
            className="hidden"
            accept=".pdf,.hwp,.pptx"
            onChange={handleFileChange}
          />
        </div>


        <div className="mt-6 flex flex-col sm:flex-row items-center justify-between border-b border-gray-100 pb-2 gap-4">
          <div className="flex bg-gray-100/80 p-1 rounded-xl w-full sm:w-auto overflow-x-auto no-scrollbar">
            <button onClick={() => setActiveTab('summary')} className={`flex-1 sm:flex-none whitespace-nowrap px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${activeTab === 'summary' ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}>
              AI 요약
            </button>
            <button onClick={() => setActiveTab('analysis')} className={`flex-1 sm:flex-none whitespace-nowrap px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${activeTab === 'analysis' ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}>
              제안서 분석
            </button>
            <button onClick={() => setActiveTab('strategy')} className={`flex-1 sm:flex-none whitespace-nowrap px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${activeTab === 'strategy' ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}>
              수주 전략
            </button>
            <button onClick={() => setActiveTab('resource')} className={`flex-1 sm:flex-none whitespace-nowrap px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${activeTab === 'resource' ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}>
              인력 배분
            </button>
          </div>
          <button
            onClick={handleDownloadPDF}
            disabled={isGeneratingPdf || !currentRFP}
            className="group flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white text-xs font-bold py-2 px-4 rounded-xl transition-all shadow-lg shadow-indigo-200 w-full sm:w-auto justify-center"
          >
            {isGeneratingPdf ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Download className="w-4 h-4 group-hover:translate-y-0.5 transition-transform" />
            )}
            <span>{isGeneratingPdf ? '생성 중...' : 'PDF 다운로드'}</span>
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto custom-scrollbar px-6 md:px-8 relative min-h-0" id="report-content">
        {isAnalyzing ? (
          <div className="absolute inset-0 bg-white/60 backdrop-blur-[2px] z-20 flex flex-col items-center justify-center space-y-4">
            <div className="relative">
              <div className="w-12 h-12 border-4 border-indigo-100 border-t-indigo-600 rounded-full animate-spin"></div>
              <Loader2 className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-5 h-5 text-indigo-600" />
            </div>
            <div className="text-center">
              <p className="text-indigo-900 text-sm font-bold animate-pulse">상세 분석 중입니다...</p>
              <p className="text-indigo-600/70 text-xs mt-2 font-medium">문서 분량에 따라 최대 3~5분 정도 소요될 수 있습니다.</p>
              <p className="text-indigo-600/50 text-[10px] mt-1">잠시만 기다려주세요 (화면을 닫지 마세요)</p>
            </div>
          </div>
        ) : currentRFP ? (
          <div className="py-2 text-gray-700 leading-relaxed animate-in fade-in slide-in-from-bottom-2 duration-500">
            {currentRFP.structuredAnalysis ? (
              <>
                {activeTab === 'summary' && <SummaryCard summary={currentRFP.structuredAnalysis.summary} />}
                {activeTab === 'analysis' && <RequirementBreakdown requirements={currentRFP.structuredAnalysis.requirements} />}
                {activeTab === 'strategy' && <StrategyView strategy={currentRFP.structuredAnalysis.strategy} />}
                {activeTab === 'resource' && (
                  <ResourceAllocationView
                    data={currentRFP.structuredAnalysis}
                    personnelList={personnelList}
                  />
                )}
              </>
            ) : (
              /* Legacy View Fallback */
              <>
                <div className="mb-4 bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-xl text-xs flex items-center gap-2">
                  <AlertCircle className="w-4 h-4" />
                  <p>이 제안서는 구 버전 형식으로 저장되었습니다. 일부 시각화 기능이 제한될 수 있습니다.</p>
                </div>
                {/* Legacy tabs omitted for brevity, but Resource Allocation unavailable here */}
                {activeTab === 'summary' && (
                  <div className="space-y-4">
                    <div className="bg-indigo-50/30 p-5 rounded-2xl border border-indigo-100/50 whitespace-pre-line text-sm">
                      {currentRFP.summary || "분석된 요약 정보가 없습니다."}
                    </div>
                  </div>
                )}
                {activeTab === 'analysis' && (
                  <div className="space-y-4">
                    <div className="bg-blue-50/30 p-5 rounded-2xl border border-blue-100/50 whitespace-pre-line text-sm">
                      {currentRFP.analysis || "분석된 상세 정보가 없습니다."}
                    </div>
                  </div>
                )}
                {activeTab === 'strategy' && (
                  <div className="space-y-4">
                    <div className="bg-violet-50/30 p-5 rounded-2xl border border-violet-100/50 whitespace-pre-line text-sm">
                      {currentRFP.strategy || "분석된 전략 정보가 없습니다."}
                    </div>
                  </div>
                )}
                {activeTab === 'resource' && (
                  <div className="p-10 text-center text-gray-400">
                    이전 버전의 분석 데이터에서는 인력 배분 기능을 사용할 수 없습니다.
                    <br />새로 분석을 진행해주세요.
                  </div>
                )}
              </>
            )}
            <div className="h-10"></div>
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-indigo-200 py-12">
            <FileText className="w-12 h-12 mb-4 opacity-20" />
            <p className="text-sm font-medium">제안서를 선택하거나 업로드 해주세요</p>
          </div>
        )}
      </div>

    </div>
  );
};

export default AnalysisPanel;
