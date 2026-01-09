import React, { useState } from 'react';
import RFPList from './components/RFPList';
import AnalysisPanel from './components/AnalysisPanel';
import TodoPanel from './components/TodoPanel';
import DashboardWidget from './components/DashboardWidget';
import Footer from './components/Footer';
import UpdatePage from './components/UpdatePage';
import LandingPage from './components/pages/LandingPage';
import { useRFP } from './hooks/useRFP';
import { LayoutDashboard, Settings, X, Key, AlertCircle, CheckCircle, Bell } from 'lucide-react';
import { checkApiHealth } from './services/apiService';

type ViewType = 'landing' | 'dashboard' | 'update';

const App: React.FC = () => {
  // Auth state - moved from useAuth hook for landing page integration
  const [apiKey, setApiKey] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [isApiHealthy, setIsApiHealthy] = useState(false);

  // Navigation state - starts at landing page
  const [view, setView] = useState<ViewType>('landing');

  const {
    rfps,
    selectedRFP,
    setSelectedRFP,
    todos,
    isAnalyzing,
    handleFileUpload,
    handleDeleteRFP
  } = useRFP(apiKey);

  // API Health check
  React.useEffect(() => {
    const checkHealth = async () => {
      const healthy = await checkApiHealth();
      setIsApiHealthy(healthy);
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  // Handler for landing page entry
  const handleEnterFromLanding = (key: string) => {
    setApiKey(key);
    setView('dashboard');
  };

  // Render Landing Page
  if (view === 'landing') {
    return <LandingPage onEnter={handleEnterFromLanding} />;
  }

  // Render Update Page
  if (view === 'update') {
    return (
      <div className="min-h-screen text-slate-900 selection:bg-indigo-100 flex flex-col">
        <UpdatePage onBack={() => setView('dashboard')} />
        <Footer />
      </div>
    );
  }

  // Render Dashboard (main view)
  return (
    <div className="min-h-screen text-slate-900 selection:bg-indigo-100 flex flex-col">
      {/* Settings Modal */}
      {showSettings && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm p-4 animate-in fade-in duration-200">
          <div className="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="p-6 border-b border-gray-100 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Settings className="w-5 h-5 text-indigo-600" />
                <h3 className="text-lg font-bold text-gray-800">Gemini API 설정</h3>
              </div>
              <button onClick={() => setShowSettings(false)} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                <X className="w-5 h-5 text-gray-500" />
              </button>
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
                    onChange={(e) => setApiKey(e.target.value)}
                    className="w-full bg-gray-50 border rounded-xl pl-11 pr-4 py-3 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all border-gray-200"
                  />
                  <Key className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                </div>
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
                onClick={() => setShowSettings(false)}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-xl shadow-lg shadow-indigo-200 transition-all active:scale-[0.98]"
              >
                설정 저장하기
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="px-8 py-5 flex items-center justify-between sticky top-0 z-50 bg-white/60 backdrop-blur-md border-b border-indigo-50">
        <div
          className="flex items-center gap-2 group cursor-pointer"
          onClick={() => setView('dashboard')}
        >
          <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-200 group-hover:rotate-12 transition-transform">
            <LayoutDashboard className="text-white w-6 h-6" />
          </div>
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-700 to-indigo-500">
            NaraStore <span className="text-indigo-400 font-medium">Analytics</span>
          </h1>
        </div>

        <div className="flex items-center gap-3">
          {/* API Key Status Indicator */}
          <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium ${apiKey ? 'bg-green-50 text-green-600 border border-green-100' : 'bg-red-50 text-red-600 border border-red-100'}`}>
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

          {/* Update Button (Notification) */}
          <button
            onClick={() => setView('update')}
            className="relative p-2.5 hover:bg-indigo-50 rounded-full transition-colors text-gray-500 hover:text-indigo-600"
            title="업데이트 노트"
          >
            <Bell className="w-5 h-5" />
            <span className="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full border border-white"></span>
          </button>

          <button
            onClick={() => setShowSettings(true)}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 rounded-full text-xs font-bold transition-all border border-indigo-100"
          >
            <Settings className="w-4 h-4" />
            <span>설정</span>
          </button>
        </div>
      </nav>

      {/* Dashboard Widget */}
      <div className="px-8 pt-6 max-w-[1600px] mx-auto">
        <DashboardWidget rfps={rfps} todos={todos} />
      </div>

      {/* Main Dashboard Layout */}
      <main className="p-8 max-w-[1600px] mx-auto flex-1">
        <div className="grid grid-cols-12 gap-8 h-[calc(100vh-230px)] min-h-[700px]">
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

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default App;
