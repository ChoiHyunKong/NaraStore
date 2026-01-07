import React, { useState, useEffect } from 'react';
import RFPList from './components/RFPList';
import AnalysisPanel from './components/AnalysisPanel';
import TodoPanel from './components/TodoPanel';
import { RFP } from './types';
import { analyzeRFP, checkApiHealth } from './services/apiService';
import { dbService } from './services/dbService';
import { LayoutDashboard, Settings, X, Key, AlertCircle, CheckCircle } from 'lucide-react';

const App: React.FC = () => {
  const [rfps, setRfps] = useState<RFP[]>([]);
  const [selectedRFP, setSelectedRFP] = useState<RFP | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [apiKeyError, setApiKeyError] = useState('');
  const [isApiHealthy, setIsApiHealthy] = useState(false);

  // Subscribe to RFPs from Firestore
  useEffect(() => {
    const unsubscribe = dbService.subscribeRFPs((updatedRFPs) => {
      setRfps(updatedRFPs);

      // If selectedRFP exists, update it with fresh data from the list
      if (selectedRFP) {
        const updatedSelected = updatedRFPs.find(r => r.id === selectedRFP.id);
        if (updatedSelected) {
          setSelectedRFP(updatedSelected);
        }
      }
    });
    return () => unsubscribe();
  }, [selectedRFP]);

  // API 서버 상태 체크
  useEffect(() => {
    const checkHealth = async () => {
      const healthy = await checkApiHealth();
      setIsApiHealthy(healthy);
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // 30초마다 체크
    return () => clearInterval(interval);
  }, []);

  // API Key가 없으면 설정 모달 자동 표시
  useEffect(() => {
    if (!apiKey) {
      setShowSettings(true);
    }
  }, []);

  const handleFileUpload = async (file: File) => {
    // API Key 체크
    if (!apiKey) {
      setApiKeyError('API Key를 먼저 입력해주세요.');
      setShowSettings(true);
      return;
    }

    setIsAnalyzing(true);
    setApiKeyError('');

    try {
      // 1. Create RFP in Firestore (Pending State)
      const docRef = await dbService.addRFP({
        title: file.name,
        analysisDate: new Date().toISOString().split('T')[0],
        status: 'pending'
      });
      const newRFPId = docRef.id;

      // Optimistic UI update (optional, but convenient) - actually subscription will catch it
      const tempRFP: RFP = {
        id: newRFPId,
        title: file.name,
        analysisDate: new Date().toISOString().split('T')[0],
        status: 'pending'
      };
      setSelectedRFP(tempRFP);

      // 2. Call Backend API
      const result = await analyzeRFP(file, apiKey);

      // 3. Update Firestore with Result
      // 3. Update Firestore with Result
      if (result.success && result.data) {
        // AI로 생성된 구조화 데이터 저장
        await dbService.updateRFP(newRFPId, {
          structuredAnalysis: result.data,
          status: 'completed',
          // 기존 필드 호환성 유지 (필요하다면)
          summary: `[프로젝트] ${result.data.summary.project_name}\n[예산] ${result.data.summary.budget}`,
          analysis: "분석 완료 (상세 리포트 확인 가능)"
        });

        // 4. Generate Auto Todos (AI generated)
        const aiTodos = result.data.todo_list || [];

        // 만약 AI가 투두를 생성하지 못했다면 기본값 사용
        const todosToInsert = aiTodos.length > 0 ? aiTodos : [
          '제안요청서(RFP) 정독 및 핵심 요구사항 파악',
          '제안팀 구성 및 역할 분담',
          '제안 목차 및 스토리보드 작성',
          '최종 제안서 리뷰 및 제출'
        ];

        for (const todoText of todosToInsert) {
          await dbService.addTodo(newRFPId, todoText);
        }

      } else {
        await dbService.updateRFP(newRFPId, {
          analysis: `[오류] ${result.error}`,
          status: 'error'
        });
        setApiKeyError(result.error || '분석 중 오류가 발생했습니다.');
      }

    } catch (error) {
      console.error("Error in upload/analysis:", error);
      setApiKeyError('처리 중 오류가 발생했습니다.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSaveApiKey = () => {
    if (!apiKey.trim()) {
      setApiKeyError('API Key를 입력해주세요.');
      return;
    }
    setApiKeyError('');
    setShowSettings(false);
  };

  const handleDeleteRFP = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation(); // prevent row click
    if (window.confirm('정말 이 제안서를 삭제하시겠습니까?\n삭제 시 분석 리포트와 To-do List가 모두 영구적으로 삭제됩니다.')) {
      try {
        await dbService.deleteRFP(id);
        if (selectedRFP?.id === id) {
          setSelectedRFP(null);
        }
      } catch (error) {
        console.error('Failed to delete RFP:', error);
        alert('삭제 중 오류가 발생했습니다.');
      }
    }
  };

  return (
    <div className="min-h-screen text-slate-900 selection:bg-indigo-100 relative">
      {/* Settings Modal */}
      {showSettings && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm p-4 animate-in fade-in duration-200">
          <div className="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="p-6 border-b border-gray-100 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Settings className="w-5 h-5 text-indigo-600" />
                <h3 className="text-lg font-bold text-gray-800">Gemini API 설정</h3>
              </div>
              {apiKey && (
                <button onClick={() => setShowSettings(false)} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              )}
            </div>

            <div className="p-6 space-y-6">
              {/* API Key Input */}
              <div>
                <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Gemini API Key</label>
                <div className="relative">
                  <input
                    type="password"
                    placeholder="AIza..."
                    value={apiKey}
                    onChange={(e) => {
                      setApiKey(e.target.value);
                      setApiKeyError('');
                    }}
                    className={`w-full bg-gray-50 border rounded-xl pl-11 pr-4 py-3 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all ${apiKeyError ? 'border-red-300' : 'border-gray-200'
                      }`}
                  />
                  <Key className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                </div>
                {apiKeyError && (
                  <p className="mt-2 text-xs text-red-500 flex items-center gap-1">
                    <AlertCircle className="w-3 h-3" />
                    {apiKeyError}
                  </p>
                )}
              </div>

              {/* API Server Status */}
              <div className="flex items-center gap-2 text-xs">
                {isApiHealthy ? (
                  <>
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span className="text-green-600 font-medium">API 서버 연결됨</span>
                  </>
                ) : (
                  <>
                    <AlertCircle className="w-4 h-4 text-yellow-500" />
                    <span className="text-yellow-600 font-medium">API 서버 연결 대기 중...</span>
                  </>
                )}
              </div>

              <div className="bg-indigo-50/50 p-4 rounded-xl border border-indigo-100">
                <p className="text-[11px] text-indigo-600 leading-relaxed font-medium">
                  * Gemini API Key는 Google AI Studio에서 발급받을 수 있습니다.<br />
                  * 입력하신 API Key는 브라우저 세션에만 유지되며, 서버에 별도로 저장되지 않습니다.
                </p>
              </div>

              <button
                onClick={handleSaveApiKey}
                disabled={!apiKey.trim()}
                className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl shadow-lg shadow-indigo-200 transition-all active:scale-[0.98]"
              >
                {apiKey ? '설정 저장하기' : 'API Key를 입력해주세요'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="px-8 py-5 flex items-center justify-between sticky top-0 z-50 bg-white/60 backdrop-blur-md border-b border-indigo-50">
        <div className="flex items-center gap-2 group cursor-pointer">
          <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-200 group-hover:rotate-12 transition-transform">
            <LayoutDashboard className="text-white w-6 h-6" />
          </div>
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-700 to-indigo-500">
            NaraStore <span className="text-indigo-400 font-medium">Analytics</span>
          </h1>
        </div>

        <div className="flex items-center gap-3">
          {/* API Key Status Indicator */}
          <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium ${apiKey ? 'bg-green-50 text-green-600 border border-green-100' : 'bg-red-50 text-red-600 border border-red-100'
            }`}>
            {apiKey ? (
              <>
                <CheckCircle className="w-3.5 h-3.5" />
                <span>API 연결됨</span>
              </>
            ) : (
              <>
                <AlertCircle className="w-3.5 h-3.5" />
                <span>API Key 필요</span>
              </>
            )}
          </div>

          <button
            onClick={() => setShowSettings(true)}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 rounded-full text-xs font-bold transition-all border border-indigo-100"
          >
            <Settings className="w-4 h-4" />
            <span>설정</span>
          </button>
        </div>
      </nav>

      {/* Main Dashboard Layout */}
      <main className="p-8 max-w-[1600px] mx-auto">
        <div className="grid grid-cols-12 gap-8 h-[calc(100vh-160px)] min-h-[700px]">
          {/* Left Panel: RFP List */}
          <div className="col-span-12 lg:col-span-4 xl:col-span-3 h-full overflow-hidden">
            <RFPList
              rfps={rfps}
              onSelectRFP={setSelectedRFP}
              selectedRFPId={selectedRFP?.id}
              onDelete={handleDeleteRFP}
            />
          </div>

          {/* Center Panel: RFP Analysis */}
          <div className="col-span-12 lg:col-span-5 xl:col-span-6 h-full overflow-hidden">
            <AnalysisPanel
              currentRFP={selectedRFP}
              onUpload={handleFileUpload}
              isAnalyzing={isAnalyzing}
              apiKeySet={!!apiKey}
            />
          </div>

          {/* Right Panel: To-do List */}
          <div className="col-span-12 lg:col-span-3 h-full overflow-hidden">
            <TodoPanel
              currentRFPId={selectedRFP?.id}
            />
          </div>
        </div>
      </main>

      {/* Footer Decoration */}
      <footer className="fixed bottom-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-20 pointer-events-none"></footer>
    </div>
  );
};

export default App;
