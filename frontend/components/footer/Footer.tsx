import React from 'react';
import { ExternalLink, Heart } from 'lucide-react';

const Footer: React.FC = () => {
    return (
        <footer className="w-full py-8 mt-auto border-t border-indigo-50 bg-white/50 backdrop-blur-sm">
            <div className="max-w-[1600px] mx-auto px-8">
                <div className="flex flex-col md:flex-row items-center justify-between gap-4">

                    {/* Copyright & Branding */}
                    <div className="flex flex-col items-center md:items-start gap-1">
                        <h2 className="text-lg font-bold text-slate-800">
                            NaraStore <span className="text-indigo-600">Analytics</span>
                        </h2>
                        <p className="text-xs text-slate-500 font-medium">
                            &copy; {new Date().getFullYear()} NaraStore Analytics. All rights reserved.
                        </p>
                    </div>

                    {/* Links */}
                    <div className="flex items-center gap-6">
                        <a
                            href="https://my-ai-lab-blog.vercel.app/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-2 px-4 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 rounded-xl transition-colors text-sm font-bold group"
                        >
                            <span>BeanLab 이동</span>
                            <ExternalLink className="w-4 h-4 group-hover:scale-110 transition-transform" />
                        </a>
                    </div>
                </div>

                {/* Tech Stack / Credits */}
                <div className="mt-8 pt-8 border-t border-indigo-50 text-center text-[11px] text-slate-400 flex items-center justify-center gap-1.5">
                    <span className="font-medium">Powered by Gemini Pro</span>
                    <span className="w-0.5 h-0.5 bg-slate-300 rounded-full"></span>
                    <span className="flex items-center gap-1">
                        Made with <Heart className="w-3 h-3 text-red-400 fill-red-400" /> by NaraStore Team
                    </span>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
