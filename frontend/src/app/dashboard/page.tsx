"use client";

import { useAnalysisViewModel } from '@/viewmodels/AnalysisViewModel';
import { useAuthViewModel } from '@/viewmodels/AuthViewModel';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function DashboardPage() {
  const { user, loading: authLoading, logout } = useAuthViewModel();
  const router = useRouter();

  const {
    text,
    setText,
    isAnalyzing,
    analysisResult,
    error,
    analyzeDocument,
    clearAnalysis,
  } = useAnalysisViewModel();

  // Protect Route
  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  if (authLoading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background text-on-surface">
        <div className="animate-pulse flex flex-col items-center">
          <span className="material-symbols-outlined text-4xl text-primary animate-spin mb-4">progress_activity</span>
          <span className="font-label tracking-widest uppercase text-sm">Authenticating...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-on-surface font-body paper-texture">
      {/* Header */}
      <header className="bg-surface-container-lowest border-b border-outline-variant/30 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <span className="font-headline italic font-bold text-2xl text-primary">LexGuard</span>
            <span className="hidden sm:inline-block px-2 py-1 bg-surface-container text-on-surface-variant text-[10px] uppercase font-label tracking-widest rounded-sm">
              Intelligence Archive
            </span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm font-label text-on-surface-variant hidden sm:block">
              {user.email}
            </span>
            <button 
              onClick={logout}
              className="text-xs font-label uppercase tracking-widest text-error hover:bg-error-container hover:text-on-error-container px-3 py-2 rounded-lg transition-colors"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      {/* Main Workspace */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
        <div className="mb-8">
          <h1 className="font-headline text-4xl font-bold text-on-surface mb-2">Legal Workspace</h1>
          <p className="text-on-surface-variant">Paste contract text below for immediate risk assessment and clause extraction.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          
          {/* Editor/Input Section */}
          <div className="bg-surface-container-lowest border border-outline-variant/30 rounded-2xl shadow-sm overflow-hidden flex flex-col h-[600px]">
            <div className="bg-surface-container-low px-4 py-3 border-b border-outline-variant/30 flex justify-between items-center">
              <span className="font-label font-semibold text-xs uppercase tracking-widest text-on-surface-variant">
                Input Document
              </span>
              <button 
                onClick={clearAnalysis}
                className="text-xs font-label uppercase tracking-wider text-secondary hover:text-on-surface transition-colors"
              >
                Clear
              </button>
            </div>
            <textarea
              className="flex-1 w-full p-6 bg-transparent border-0 focus:ring-0 resize-none font-body text-sm leading-relaxed text-on-surface placeholder:text-outline"
              placeholder="Paste the terms of service, NDA, or contract text here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <div className="p-4 bg-surface-container-low border-t border-outline-variant/30">
              <button
                onClick={() => analyzeDocument(text)}
                disabled={isAnalyzing || !text.trim()}
                className="w-full flex justify-center items-center gap-2 py-3 bg-gradient-to-r from-primary to-primary-container text-on-primary font-label font-bold tracking-widest uppercase text-sm rounded-xl hover:opacity-90 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isAnalyzing ? (
                  <>
                    <span className="material-symbols-outlined animate-spin text-[20px]">progress_activity</span>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <span className="material-symbols-outlined text-[20px]">troubleshoot</span>
                    Run Risk Analysis
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Results Section */}
          <div className="bg-surface-container-lowest border border-outline-variant/30 rounded-2xl shadow-sm overflow-hidden flex flex-col h-[600px]">
             <div className="bg-surface-container-low px-4 py-3 border-b border-outline-variant/30 flex items-center gap-2">
              <span className="material-symbols-outlined text-primary text-[20px]">psychiatry</span>
              <span className="font-label font-semibold text-xs uppercase tracking-widest text-on-surface-variant">
                LexGuard Intelligence Report
              </span>
            </div>
            
            <div className="flex-1 overflow-y-auto p-6">
              {error && (
                <div className="bg-error-container text-on-error-container p-4 rounded-xl border border-error/20 mb-4 flex items-start gap-3">
                  <span className="material-symbols-outlined text-error">error</span>
                  <p className="text-sm font-medium">{error}</p>
                </div>
              )}

              {!analysisResult && !isAnalyzing && !error && (
                <div className="h-full flex flex-col items-center justify-center text-center text-outline px-8">
                  <span className="material-symbols-outlined text-6xl mb-4 opacity-50">contract</span>
                  <p className="font-body text-sm">
                    The report will appear here once the analysis is complete.
                  </p>
                </div>
              )}

              {isAnalyzing && (
                <div className="h-full flex flex-col items-center justify-center text-center text-primary px-8">
                  <span className="material-symbols-outlined text-6xl mb-4 animate-pulse">auto_awesome</span>
                  <h3 className="font-headline text-xl font-bold mb-2">Analyzing Document</h3>
                  <p className="font-body text-sm text-on-surface-variant">
                    Running text through Gemini models to identify potential legal risks and extract key clauses...
                  </p>
                </div>
              )}

              {analysisResult && (
                <div className="prose prose-sm prose-slate max-w-none">
                  {/* Using white-space pre-wrap so Markdown-ish text from Gemini formats correctly */}
                  <div className="whitespace-pre-wrap font-body text-sm leading-relaxed text-on-surface">
                    {analysisResult}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
