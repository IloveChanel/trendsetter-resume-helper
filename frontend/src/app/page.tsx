
'use client';

import { useState, useEffect } from 'react';
import './style.css'; 

export default function Home() {
    // --- 1. CORE DATA (Same as GitHub resumeStudio) ---
    const [jobTitle, setJobTitle] = useState('');
    const [jobDesc, setJobDesc] = useState('');
    const [originalResumeText, setOriginalResumeText] = useState('');
    const [generatedResume, setGeneratedResume] = useState('');
    const [fileName, setFileName] = useState('');
    const [loading, setLoading] = useState(false);
    const [atsScore, setAtsScore] = useState(0);

    // --- 2. BACKEND LOGIC (Same as GitHub runAnalysis) ---
    async function runAnalysis() {
        if (!jobDesc.trim()) {
            alert('🚨 Please provide a job description for ATS analysis!');
            return;
        }
        setLoading(true);
        try {
            const getApiUrl = () => {
                const hostname = window.location.hostname;
                if (hostname === 'localhost' || hostname === '127.0.0.1') return 'http://localhost:8000';
                return 'https://trendsetter-resume-helper.onrender.com';
            };

            const formData = new FormData();
            formData.append('resume_text', originalResumeText || 'Generate new');
            formData.append('job_description', jobDesc);
            formData.append('job_title', jobTitle);

            const response = await fetch(`${getApiUrl()}/api/match-job`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            setGeneratedResume(data.optimized_resume || data.enhanced_text || '');
            setAtsScore(data.ats_score || 0);
            alert('✅ Analysis Complete!');
        } catch (error) {
            console.error("Analysis Failed:", error);
            alert('Analysis Error. Is the backend server running?');
        } finally {
            setLoading(false);
        }
    }

    // --- 3. UI RENDER (Keeping all GitHub Tailwind classes) ---
    return (
        <div className="relative min-h-screen flex flex-col text-white">
            {/* Background Layer from GitHub */}
            <div className="fixed top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_50%_50%,rgba(17,24,39,1)_0%,rgba(5,5,5,1)_100%)] -z-10"></div>
            <div className="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/10 blur-[120px] rounded-full"></div>

            <header className="px-8 py-6 flex justify-between items-center border-b border-white/5">
                <div className="text-xl font-bold tracking-tighter uppercase">Trendsetter<span className="text-blue-500">AI</span></div>
                <button onClick={() => window.location.reload()} className="text-xs text-gray-500 hover:text-white uppercase tracking-widest transition-colors">New Project</button>
            </header>

            <main className="flex-1 grid lg:grid-cols-2 gap-0">
                {/* Left Section (Resume Input) */}
                <section className="p-6 lg:p-12 border-r border-white/5 flex flex-col space-y-6 overflow-y-auto">
                    <div className="space-y-4">
                        <h2 className="text-sm font-bold text-gray-500 uppercase tracking-[0.2em]">1. Upload Resume</h2>
                        <div className="glass p-6 rounded-2xl border-dashed border-white/10 flex flex-col items-center justify-center cursor-pointer hover:border-blue-500/50 transition-all">
                            <input type="file" className="hidden" id="fileInput" onChange={(e) => setFileName(e.target.files?.[0]?.name || '')} />
                            <label htmlFor="fileInput" className="text-center cursor-pointer w-full">
                                <span className="text-2xl mb-2 block">📄</span>
                                <span className="text-xs text-gray-400">{fileName || 'Click to upload PDF, DOC, or TXT'}</span>
                            </label>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <h2 className="text-sm font-bold text-gray-500 uppercase tracking-[0.2em]">OR Paste Text</h2>
                        <textarea 
                            value={originalResumeText}
                            onChange={(e) => setOriginalResumeText(e.target.value)}
                            className="w-full h-64 bg-white/5 border border-white/10 p-4 rounded-xl text-sm focus:border-blue-500/50 transition-all resize-none outline-none"
                            placeholder="Paste resume content..."
                        />
                    </div>
                </section>

                {/* Right Section (Job Details & Analysis) */}
                <section className="p-6 lg:p-12 bg-black/20 space-y-8 overflow-y-auto">
                    <div className="space-y-4">
                        <h2 className="text-sm font-bold text-gray-500 uppercase tracking-[0.2em]">2. Target Job Title</h2>
                        <input 
                            value={jobTitle}
                            onChange={(e) => setJobTitle(e.target.value)}
                            className="w-full bg-white/5 border border-white/10 p-4 rounded-xl text-sm focus:border-blue-500/50 outline-none transition-all"
                            placeholder="e.g. Senior Software Engineer"
                        />
                    </div>

                    <div className="space-y-4">
                        <h2 className="text-sm font-bold text-gray-500 uppercase tracking-[0.2em]">3. Job Description</h2>
                        <textarea 
                            value={jobDesc}
                            onChange={(e) => setJobDesc(e.target.value)}
                            className="w-full h-40 bg-white/5 border border-white/10 p-4 rounded-xl text-sm focus:border-blue-500/50 transition-all resize-none outline-none"
                            placeholder="Paste requirements..."
                        />
                    </div>

                    <button 
                        onClick={runAnalysis}
                        disabled={loading || !jobDesc.trim()}
                        className={`w-full py-5 rounded-2xl font-black text-lg uppercase tracking-tighter transition-all ${
                            !jobDesc.trim() ? 'bg-gray-600 text-gray-400 cursor-not-allowed' : 
                            loading ? 'bg-yellow-600 text-yellow-100' : 'bg-white text-black hover:bg-blue-600 hover:text-white'
                        }`}
                    >
                        {loading ? '⚡ AI Processing...' : '🤖 Analyze & Optimize'}
                    </button>
                    
                    {/* Score Display */}
                    {atsScore > 0 && (
                        <div className="glass p-6 rounded-2xl text-center">
                            <div className="text-4xl font-bold text-blue-500">{atsScore}%</div>
                            <div className="text-xs uppercase tracking-widest text-gray-400 mt-2">ATS Compatibility Score</div>
                        </div>
                    )}
                </section>
            </main>
        </div>
    );
}