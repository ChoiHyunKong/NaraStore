import React from 'react';
import { Github, Mail, ShieldCheck } from 'lucide-react';

const Footer: React.FC = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="mt-auto border-t border-indigo-50 bg-white/40 backdrop-blur-sm">
            <div className="max-w-[1600px] mx-auto px-8 py-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
                    {/* Brand Info */}
                    <div className="space-y-2">
                        <div className="flex items-center gap-2">
                            <ShieldCheck className="w-5 h-5 text-indigo-600" />
                            <span className="font-bold text-gray-800">NaraStore Analytics</span>
                        </div>
                        <p className="text-xs text-gray-500">
                            AI-Powered RFP Analysis Platform<br />
                            Powered by Google Gemini 3.0 Flash
                        </p>
                    </div>

                    {/* Links - Center */}
                    <div className="flex justify-center gap-6">
                        <a href="#" className="text-gray-400 hover:text-indigo-600 transition-colors text-sm font-medium">이용약관</a>
                        <a href="#" className="text-gray-400 hover:text-indigo-600 transition-colors text-sm font-medium">개인정보처리방침</a>
                        <a href="#" className="text-gray-400 hover:text-indigo-600 transition-colors text-sm font-medium">도움말</a>
                    </div>

                    {/* Social / Copyright - Right */}
                    <div className="flex flex-col items-end gap-3">
                        <div className="flex items-center gap-3">
                            <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="p-2 bg-gray-100 hover:bg-gray-200 rounded-full transition-colors">
                                <Github className="w-4 h-4 text-gray-600" />
                            </a>
                            <a href="mailto:support@narastore.com" className="p-2 bg-gray-100 hover:bg-gray-200 rounded-full transition-colors">
                                <Mail className="w-4 h-4 text-gray-600" />
                            </a>
                        </div>
                        <p className="text-[10px] text-gray-400 font-medium">
                            © {currentYear} NaraStore Corp. All rights reserved.
                        </p>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
