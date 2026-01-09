import React from 'react';
import { ArrowLeft, Rocket, Zap, Bug, CheckCircle2 } from 'lucide-react';

interface UpdatePageProps {
    onBack: () => void;
}

const updates = [
    {
        version: "v1.2.0",
        date: "2026. 01. 09",
        type: "major", // major, feature, fix
        title: "Gemini 3.0 Flash 미리보기 적용, 성능 최적화",
        items: [
            { type: "new", text: "Google Gemini 3.0 Flash Preview 모델 탑재로 분석 속도/정확도 향상" },
            { type: "improve", text: "대시보드 라이브 데이터 구독 최적화 (버벅거림 해결)" },
            { type: "fix", text: "그래프 툴팁 마우스 추적 시 딜레이 현상 수정" },
            { type: "new", text: "앱 전반적인 UI/UX 개선 (Glassmorphism 강화)" }
        ]
    },
    {
        version: "v1.1.5",
        date: "2026. 01. 08",
        type: "feature",
        title: "대시보드 위젯 및 통계 기능 추가",
        items: [
            { type: "new", text: "메인 화면에 RFP/Todo 현황 대시보드 위젯 추가" },
            { type: "new", text: "활동 추이 그래프(7일/1개월/1년) 시각화" },
            { type: "improve", text: "설정 모달 디자인 리뉴얼" }
        ]
    }
];

const UpdatePage: React.FC<UpdatePageProps> = ({ onBack }) => {
    return (
        <div className="min-h-screen bg-gray-50/50">
            {/* Header */}
            <div className="bg-white border-b border-gray-100 py-6 px-4 md:px-8">
                <div className="max-w-4xl mx-auto flex items-center justify-between">
                    <button
                        onClick={onBack}
                        className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 rounded-xl transition-all font-medium"
                    >
                        <ArrowLeft className="w-5 h-5" />
                        <span>돌아가기</span>
                    </button>
                    <div className="flex items-center gap-2">
                        <Rocket className="w-5 h-5 text-indigo-600" />
                        <h1 className="text-xl font-bold text-gray-800">업데이트 노트</h1>
                    </div>
                    <div className="w-24"></div> {/* Spacer for centering */}
                </div>
            </div>

            {/* Content using Carousel Style Layout */}
            <div className="max-w-3xl mx-auto px-6 py-12 space-y-12">
                {updates.map((update, index) => (
                    <div key={index} className="relative pl-8 md:pl-0">
                        {/* Timeline Line */}
                        <div className="absolute left-0 top-0 bottom-0 w-px bg-indigo-100 md:left-[-40px]"></div>

                        {/* Timeline Dot */}
                        <div className="absolute left-[-4px] top-6 w-2.5 h-2.5 rounded-full bg-indigo-600 border-2 border-white ring-4 ring-indigo-50 md:left-[-45px]"></div>

                        <div className="glass-card bg-white rounded-3xl p-8 border border-white/60 shadow-xl shadow-indigo-100/50 hover:shadow-indigo-100/80 transition-shadow">
                            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                                <div>
                                    <div className="flex items-center gap-3 mb-2">
                                        <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide ${update.type === 'major' ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200' :
                                                update.type === 'feature' ? 'bg-emerald-500 text-white shadow-md shadow-emerald-200' :
                                                    'bg-gray-500 text-white'
                                            }`}>
                                            {update.type}
                                        </span>
                                        <span className="text-sm font-bold text-indigo-900">{update.version}</span>
                                    </div>
                                    <h2 className="text-xl font-bold text-gray-800">{update.title}</h2>
                                </div>
                                <span className="text-sm font-semibold text-gray-400 bg-gray-50 px-3 py-1 rounded-lg">
                                    {update.date}
                                </span>
                            </div>

                            <ul className="space-y-4">
                                {update.items.map((item, i) => (
                                    <li key={i} className="flex items-start gap-3">
                                        <div className="mt-0.5 min-w-[20px]">
                                            {item.type === 'new' && <Zap className="w-5 h-5 text-amber-500" />}
                                            {item.type === 'improve' && <CheckCircle2 className="w-5 h-5 text-emerald-500" />}
                                            {item.type === 'fix' && <Bug className="w-5 h-5 text-rose-500" />}
                                        </div>
                                        <p className="text-sm text-gray-600 leading-relaxed font-medium">
                                            {item.text}
                                        </p>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                ))}

                <div className="text-center py-12">
                    <p className="text-gray-400 text-sm font-medium">모든 업데이트 내역을 확인했습니다.</p>
                </div>
            </div>
        </div>
    );
};

export default UpdatePage;
