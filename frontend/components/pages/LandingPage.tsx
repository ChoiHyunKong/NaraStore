import React, { useState, useEffect, useRef } from 'react';
import { LayoutDashboard, ArrowRight, DollarSign, Target, Activity, Sparkles, FileSearch, TrendingUp } from 'lucide-react';

interface LandingPageProps {
    onEnter: (apiKey: string) => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onEnter }) => {
    const [apiKey, setApiKey] = useState('');
    const [counterValue, setCounterValue] = useState(0);
    const [winningProb, setWinningProb] = useState(0);
    const [isLoaded, setIsLoaded] = useState(false);
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // Counter animations
    useEffect(() => {
        setIsLoaded(true);
        const vInt = setInterval(() => setCounterValue(v => v >= 1.24 ? 1.24 : v + 0.02), 30);
        const pInt = setInterval(() => setWinningProb(p => p >= 92 ? 92 : p + 1), 20);
        return () => { clearInterval(vInt); clearInterval(pInt); };
    }, []);

    // Particle animation
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrameId: number;
        let particles: { x: number; y: number; vx: number; vy: number; size: number }[] = [];

        const init = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            particles = Array.from({ length: 60 }, () => ({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.3,
                vy: (Math.random() - 0.5) * 0.3,
                size: Math.random() * 1.5 + 0.5
            }));
        };

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = 'rgba(79, 70, 229, 0.2)'; // Increased opacity for lines
            ctx.fillStyle = 'rgba(79, 70, 229, 0.3)'; // Increased opacity for particles

            particles.forEach((p, i) => {
                p.x += p.vx;
                p.y += p.vy;
                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();

                for (let j = i + 1; j < particles.length; j++) {
                    const p2 = particles[j];
                    const dist = Math.sqrt((p.x - p2.x) ** 2 + (p.y - p2.y) ** 2);
                    if (dist < 200) {
                        ctx.beginPath();
                        ctx.lineWidth = 0.5 * (1 - dist / 200);
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.stroke();
                    }
                }
            });
            animationFrameId = requestAnimationFrame(animate);
        };

        init();
        animate();
        window.addEventListener('resize', init);

        return () => {
            cancelAnimationFrame(animationFrameId);
            window.removeEventListener('resize', init);
        };
    }, []);

    const handleStart = () => {
        onEnter(apiKey);
    };

    return (
        <div className="relative min-h-screen w-full flex flex-col items-center justify-center overflow-hidden bg-slate-50">
            {/* Particle Canvas Background */}
            <canvas ref={canvasRef} className="absolute inset-0 z-0" />

            {/* Floating Module - Left */}
            <div className="absolute top-[15%] left-[10%] hidden 2xl:block z-10">
                <div className="glass-card p-5 rounded-3xl shadow-2xl shadow-indigo-200/40 bg-white/95 backdrop-blur-xl border border-white/30">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="w-8 h-8 bg-blue-700 rounded-xl flex items-center justify-center text-white">
                            <DollarSign className="w-4 h-4" />
                        </div>
                        <div>
                            <div className="text-[8px] font-black text-slate-600 uppercase">Market Value</div>
                            <div className="text-lg font-black text-slate-900">${counterValue.toFixed(2)}B</div>
                        </div>
                    </div>
                    <div className="w-32 bg-slate-200 h-1.5 rounded-full overflow-hidden">
                        <div
                            className="bg-blue-700 h-full transition-all duration-1000"
                            style={{ width: isLoaded ? '74%' : '0%' }}
                        />
                    </div>
                </div>
            </div>

            {/* Floating Module - Right */}
            <div className="absolute bottom-[20%] right-[10%] hidden 2xl:block z-10">
                <div className="glass-card p-5 rounded-3xl shadow-2xl shadow-indigo-200/40 bg-white/95 backdrop-blur-xl border border-white/30">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="w-8 h-8 bg-indigo-700 rounded-xl flex items-center justify-center text-white">
                            <Target className="w-4 h-4" />
                        </div>
                        <div className="text-[8px] font-black text-slate-600 uppercase">Winning Prob.</div>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="text-3xl font-black text-indigo-700">{winningProb}%</div>
                        <Activity className="w-5 h-5 text-emerald-600 animate-pulse" />
                    </div>
                </div>
            </div>

            {/* Main UI */}
            <div className="relative z-20 w-full max-w-lg px-6 text-center flex flex-col items-center">
                {/* Logo & Title */}
                <div className="flex items-center justify-center gap-4 mb-4 whitespace-nowrap">
                    <div className="w-12 h-12 bg-indigo-600 rounded-2xl flex items-center justify-center shadow-xl shadow-indigo-200">
                        <LayoutDashboard className="text-white w-7 h-7" />
                    </div>
                    <h1 className="text-3xl md:text-5xl font-black tracking-tighter text-slate-900">
                        NaraStore <span className="text-indigo-600">Analytics</span>
                    </h1>
                </div>

                <p className="text-base text-slate-500 mb-10 font-medium">
                    제안서 데이터를 수주 전략으로 변환하는<br />지능형 정밀 분석 시스템
                </p>

                {/* Login Card */}
                <div className="glass-card w-full p-8 md:p-10 rounded-[2.5rem] shadow-2xl bg-white/95 backdrop-blur-xl border border-white/30">
                    <div className="space-y-6 text-left">
                        {/* AI Engine Selection */}
                        <div>
                            <label className="block text-[10px] font-black text-indigo-300 uppercase mb-3">
                                AI Engine Selection
                            </label>
                            <select className="w-full bg-indigo-50/30 border-0 rounded-2xl px-6 py-4 text-sm font-bold text-indigo-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
                                <option>Gemini 3 Pro (Vision)</option>
                                <option>GPT-4o Enterprise</option>
                            </select>
                        </div>

                        {/* API Key Input */}
                        <div>
                            <label className="block text-[10px] font-black text-indigo-300 uppercase mb-3">
                                API Authentication
                            </label>
                            <input
                                type="password"
                                placeholder="API Key를 입력하세요"
                                value={apiKey}
                                onChange={(e) => setApiKey(e.target.value)}
                                className="w-full bg-indigo-50/30 border-0 rounded-2xl px-6 py-4 text-sm font-bold text-indigo-900 placeholder:text-indigo-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                            />
                        </div>

                        {/* Enter Button */}
                        <button
                            onClick={handleStart}
                            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 rounded-2xl flex items-center justify-center gap-2 transition-all active:scale-[0.98] shadow-lg shadow-indigo-200"
                        >
                            분석 대시보드 진입
                            <ArrowRight className="w-4 h-4" />
                        </button>

                        {/* Skip Link */}
                        <button
                            onClick={() => onEnter('')}
                            className="w-full text-center text-xs text-slate-400 hover:text-indigo-600 font-medium transition-colors"
                        >
                            API Key 없이 시작하기 (Mock Mode)
                        </button>
                    </div>
                </div>

                {/* Feature Cards */}
                <div className="mt-12 grid grid-cols-3 gap-4 w-full">
                    <div className="bg-white/80 backdrop-blur-sm p-4 rounded-2xl text-center border border-white/50 shadow-lg shadow-indigo-50">
                        <div className="w-10 h-10 mx-auto mb-2 bg-indigo-100 rounded-xl flex items-center justify-center">
                            <Sparkles className="w-5 h-5 text-indigo-600" />
                        </div>
                        <div className="text-[10px] font-bold text-slate-600">AI 분석</div>
                    </div>
                    <div className="bg-white/80 backdrop-blur-sm p-4 rounded-2xl text-center border border-white/50 shadow-lg shadow-indigo-50">
                        <div className="w-10 h-10 mx-auto mb-2 bg-emerald-100 rounded-xl flex items-center justify-center">
                            <FileSearch className="w-5 h-5 text-emerald-600" />
                        </div>
                        <div className="text-[10px] font-bold text-slate-600">RFP 정밀검토</div>
                    </div>
                    <div className="bg-white/80 backdrop-blur-sm p-4 rounded-2xl text-center border border-white/50 shadow-lg shadow-indigo-50">
                        <div className="w-10 h-10 mx-auto mb-2 bg-amber-100 rounded-xl flex items-center justify-center">
                            <TrendingUp className="w-5 h-5 text-amber-600" />
                        </div>
                        <div className="text-[10px] font-bold text-slate-600">수주 전략</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LandingPage;
