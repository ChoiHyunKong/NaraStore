import React from 'react';
import { ArrowLeft, Rocket, Zap, Bug, CheckCircle2 } from 'lucide-react';

interface UpdatePageProps {
    onBack: () => void;
}

const updates = [
    {
        version: "v1.5.0",
        date: "2026. 01. 11",
        type: "major",
        title: "수주 전략 분석 고도화 및 인사이트 강화",
        items: [
            { type: "new", text: "전략적 인사이트 3대 요소 추가 (앵커 포인트, 차별화 요소, 리스크 완화)" },
            { type: "improve", text: "수주 전략 리포트 UI 전면 개편 (가독성 높은 카드형 레이아웃)" },
            { type: "improve", text: "AI 분석 엔진 고도화: 발주처 의도 파악 및 맞춤형 전략 도출 능력 강화" },
            { type: "fix", text: "분석 결과 캐싱 시 누락된 필드 자동 보완 로직 개선" }
        ]
    },
    {
        version: "v1.4.0",
        date: "2026. 01. 11",
        type: "major",
        title: "AI 분석 요약 기능 고도화 및 디자인 개선",
        items: [
            { type: "new", text: "핵심 키워드(#태그) 및 발주처 중점 포인트 자동 추출 기능 추가" },
            { type: "improve", text: "AI 분석 요약 디자인 리뉴얼 (가독성 강화, 깔끔한 해시태그 스타일)" },
            { type: "improve", text: "분석 데이터 누락 방지 로직 적용 (자동 보완 기능)" },
            { type: "improve", text: "제안요청서 분석 프롬프트 고도화 (정확도 향상)" },
            { type: "improve", text: "요구사항 추출 정확도 대폭 개선 (완전성, 구체성, 중복 제거 강화)" }
        ]
    },
    {
        version: "v1.3.1",
        date: "2026. 01. 10",
        type: "feature",
        title: "회사 인력 현황 관리 기능 추가 및 안정화",
        items: [
            { type: "new", text: "인력 현황 대시보드 및 등록/관리 기능 추가" },
            { type: "improve", text: "제안서 분석 엔진 안정성 강화 (오류 복구)" },
            { type: "improve", text: "인원 등록/삭제 사용자 경험(UX) 개선" },
            { type: "fix", text: "로그인 시 분석실로 자동 이동하도록 개선" }
        ]
    },
    {
        version: "v1.3.0",
        date: "2026. 01. 10",
        type: "major",
        title: "랜딩 페이지 도입 및 페이지 구조 개편",
        items: [
            { type: "new", text: "신규 랜딩 페이지 추가 (API Key 입력 및 소개)" },
            { type: "improve", text: "페이지 라우팅 구조 개선 (랜딩 → 대시보드 → 분석)" },
            { type: "improve", text: "배경 파티클 애니메이션 시각적 개선" },
            { type: "new", text: "업데이트 노트 디자인 개선 (개조식)" }
        ]
    },
    {
        version: "v1.2.0",
        date: "2026. 01. 09",
        type: "major", // major, feature, fix
        title: "Gemini 3.0 Flash 미리보기 적용, 성능 최적화",
        items: [
            { type: "new", text: "Google Gemini 3.0 Flash Preview 모델 탑재" },
            { type: "improve", text: "분석 속도 및 정확도 향상" },
            { type: "improve", text: "대시보드 라이브 데이터 구독 최적화" },
            { type: "fix", text: "그래프 툴팁 마우스 추적 딜레이 현상 수정" },
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
        <div className="h-screen overflow-hidden bg-gray-50/50">
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
            <div className="max-w-3xl mx-auto px-6 py-12 space-y-12 h-[calc(100vh-88px)] overflow-y-auto custom-scrollbar">
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
