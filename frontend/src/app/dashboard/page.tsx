"use client";

import { useAnalysisViewModel } from '@/viewmodels/AnalysisViewModel';
import { useAuthViewModel } from '@/viewmodels/AuthViewModel';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

/**
 * Returns display metadata for a given file extension.
 * @param fileName - The name of the file to inspect.
 * @returns Object with a Material Symbol icon name and human-readable label.
 */
const getFileDetails = (fileName: string): { icon: string; label: string } => {
  const ext = fileName.split('.').pop()?.toLowerCase();
  switch (ext) {
    case 'pdf':  return { icon: 'picture_as_pdf', label: 'PDF Document' };
    case 'docx': return { icon: 'description', label: 'Word Document' };
    case 'txt':  return { icon: 'article', label: 'Text Document' };
    case 'png':
    case 'jpg':
    case 'jpeg': return { icon: 'image', label: 'Document Image' };
    default:     return { icon: 'draft', label: 'Document' };
  }
};

export default function DashboardPage() {
  const { user, loading: authLoading, logout } = useAuthViewModel();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'report' | 'chat'>('report');

  const {
    text,
    setText,
    file,
    setFile,
    isAnalyzing,
    analysisResult,
    error,
    chatMessages,
    isChatting,
    chatInput,
    setChatInput,
    analyzeDocument,
    sendChatMessage,
    clearAnalysis,
  } = useAnalysisViewModel();

  // Protect Route: redirect unauthenticated users to login
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

  const fileDetails = file ? getFileDetails(file.name) : null;

  return (
    <div className="min-h-screen bg-background text-on-surface font-body paper-texture">
      {/* Header */}
      <header className="bg-surface-container-lowest/80 backdrop-blur-md border-b border-outline-variant/15 sticky top-0 z-50">
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
              className="text-xs font-label uppercase tracking-widest text-error bg-surface-container-low hover:bg-error-container/40 hover:text-error px-3.5 py-2.5 rounded-lg transition-all"
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
          <p className="font-headline text-on-surface-variant">Paste contract text below for immediate risk assessment and clause extraction.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          
          {/* Editor/Input Section */}
          <div className="bg-surface-container-lowest border border-outline-variant/15 rounded-2xl shadow-sm overflow-hidden flex flex-col h-[600px] hover:shadow-md transition-shadow duration-200">
            <div className="bg-surface-container-low/50 px-4 py-3 border-b border-outline-variant/15 flex justify-between items-center">
              <span className="font-label font-semibold text-xs uppercase tracking-widest text-on-surface-variant">
                Input Document
              </span>
              <div className="flex items-center gap-3">
                <input
                  type="file"
                  id="file-upload"
                  accept="application/pdf,.docx,text/plain,image/png,image/jpeg"
                  className="hidden"
                  onChange={(e) => {
                    if (e.target.files && e.target.files[0]) {
                      setFile(e.target.files[0]);
                      setText('');
                    }
                  }}
                />
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer text-xs font-label uppercase tracking-wider text-primary hover:text-primary-container transition-colors flex items-center gap-1"
                >
                  <span className="material-symbols-outlined text-[16px]">upload_file</span>
                  {file ? 'Change File' : 'Upload File'}
                </label>
                <button 
                  onClick={clearAnalysis}
                  className="text-xs font-label uppercase tracking-wider text-secondary hover:text-on-surface transition-colors"
                >
                  Clear
                </button>
              </div>
            </div>
            {file ? (
              <div className="flex-1 flex flex-col items-center justify-center p-6 bg-surface-container-low/30 border-2 border-dashed border-outline-variant/20 m-4 rounded-xl">
                <span className="material-symbols-outlined text-6xl text-primary mb-4 opacity-80">{fileDetails?.icon ?? 'draft'}</span>
                <p className="font-headline font-semibold text-lg text-on-surface text-center break-all">{file.name}</p>
                <p className="text-sm text-on-surface-variant mt-2">{(file.size / 1024 / 1024).toFixed(2)} MB &mdash; {fileDetails?.label ?? 'Document'} ready.</p>
                <button
                  onClick={() => setFile(null)}
                  className="mt-6 px-4 py-2 bg-error-container text-on-error-container text-xs font-label uppercase tracking-widest rounded-lg hover:bg-error hover:text-on-error transition-colors"
                >
                  Remove File
                </button>
              </div>
            ) : (
              <textarea
                className="flex-1 w-full p-6 bg-transparent border-0 focus:ring-0 resize-none font-body text-sm leading-relaxed text-on-surface placeholder:text-outline/70"
                placeholder="Paste the terms of service, NDA, or contract text here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
              />
            )}
            <div className="p-4 bg-surface-container-low/50 border-t border-outline-variant/15">
              <button
                onClick={() => analyzeDocument()}
                disabled={isAnalyzing || (!text.trim() && !file)}
                className="w-full flex justify-center items-center gap-2 py-3.5 bg-gradient-to-r from-primary to-primary-container text-on-primary font-label font-bold tracking-widest uppercase text-sm rounded-xl hover:opacity-95 hover:scale-[1.01] hover:-translate-y-0.5 active:scale-[0.99] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none shadow-sm"
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
          <div className="bg-surface-container-lowest border border-outline-variant/15 rounded-2xl shadow-sm overflow-hidden flex flex-col h-[600px] hover:shadow-md transition-shadow duration-200">
            <div className="bg-surface-container-low/50 px-4 py-2.5 border-b border-outline-variant/15 flex justify-between items-center">
              <div className="flex gap-2">
                <button
                  onClick={() => setActiveTab('report')}
                  className={`px-3.5 py-2 rounded-lg text-xs font-label uppercase tracking-widest transition-all ${
                    activeTab === 'report'
                      ? 'bg-gradient-to-r from-primary to-primary-container text-on-primary font-bold shadow-sm'
                      : 'bg-surface-container-high/60 text-on-surface-variant hover:bg-surface-container-highest'
                  }`}
                >
                  Report
                </button>
                <button
                  onClick={() => setActiveTab('chat')}
                  disabled={!analysisResult}
                  className={`px-3.5 py-2 rounded-lg text-xs font-label uppercase tracking-widest transition-all disabled:opacity-50 disabled:cursor-not-allowed ${
                    activeTab === 'chat'
                      ? 'bg-gradient-to-r from-primary to-primary-container text-on-primary font-bold shadow-sm'
                      : 'bg-surface-container-high/60 text-on-surface-variant hover:bg-surface-container-highest'
                  }`}
                >
                  Q&A Chat
                </button>
              </div>
              <span className="font-label font-semibold text-[10px] uppercase tracking-widest text-outline">
                {activeTab === 'report' ? 'Report Mode' : 'Chat Mode'}
              </span>
            </div>
            
            <div className="flex-1 overflow-y-auto p-6 flex flex-col justify-between">
              <div className="flex-1 overflow-y-auto mb-4">
                {error && (
                  <div className="bg-error-container/20 text-error p-4 rounded-xl border border-error/15 mb-4 flex items-start gap-3">
                    <span className="material-symbols-outlined text-error">error</span>
                    <p className="text-sm font-medium">{error}</p>
                  </div>
                )}

                {!analysisResult && !isAnalyzing && !error && (
                  <div className="h-full flex flex-col items-center justify-center text-center text-outline px-8 py-20">
                    <span className="material-symbols-outlined text-6xl mb-4 opacity-50">contract</span>
                    <p className="font-body text-sm">
                      The report will appear here once the analysis is complete.
                    </p>
                  </div>
                )}

                {isAnalyzing && (
                  <div className="h-full flex flex-col items-center justify-center text-center text-primary px-8 py-20">
                    <span className="material-symbols-outlined text-6xl mb-4 animate-pulse">auto_awesome</span>
                    <h3 className="font-headline text-xl font-bold mb-2">Analyzing Document</h3>
                    <p className="font-headline text-sm text-on-surface-variant">
                      Running text through Gemini models to identify potential legal risks and extract key clauses...
                    </p>
                  </div>
                )}

                {analysisResult && activeTab === 'report' && (
                  <div className="prose prose-sm prose-slate max-w-none">
                    {/* Using white-space pre-wrap so Markdown-ish text from Gemini formats correctly */}
                    <div className="whitespace-pre-wrap font-headline text-sm leading-relaxed text-on-surface">
                      {analysisResult}
                    </div>
                  </div>
                )}

                {analysisResult && activeTab === 'chat' && (
                  <div className="flex flex-col gap-4">
                    <div className="bg-tertiary-container/15 p-3.5 rounded-xl border border-tertiary/15 text-xs text-tertiary font-headline font-semibold italic">
                      💬 Ask specific questions about this contract. (e.g., &quot;What is the notice period for termination?&quot;)
                    </div>
                    {chatMessages.map((msg, i) => (
                      <div
                        key={i}
                        className={`flex flex-col max-w-[80%] rounded-xl p-3 text-sm leading-relaxed ${
                          msg.sender === 'user'
                            ? 'bg-gradient-to-r from-primary to-primary-container text-on-primary self-end shadow-sm'
                            : 'bg-surface-container-high/50 text-on-surface self-start border border-outline-variant/15'
                        }`}
                      >
                        <span className="font-label text-[10px] uppercase opacity-70 mb-1">
                          {msg.sender === 'user' ? 'You' : 'LexGuard AI'}
                        </span>
                        <div className="whitespace-pre-wrap">{msg.text}</div>
                      </div>
                    ))}
                    {isChatting && (
                      <div className="bg-surface-container-high/50 text-on-surface self-start border border-outline-variant/15 rounded-xl p-3 max-w-[80%] flex items-center gap-2">
                        <span className="animate-pulse font-label text-xs uppercase tracking-widest text-on-surface-variant">Thinking...</span>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {analysisResult && activeTab === 'chat' && (
                <div className="pt-4 border-t border-outline-variant/15 flex gap-2">
                  <input
                    type="text"
                    className="flex-1 bg-surface-container-low/70 border border-outline-variant/15 rounded-xl px-4 py-3 text-sm font-body text-on-surface focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary placeholder:text-outline/70 transition-all"
                    placeholder="Ask a question about the document..."
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') sendChatMessage();
                    }}
                  />
                  <button
                    onClick={sendChatMessage}
                    disabled={isChatting || !chatInput.trim()}
                    className="bg-gradient-to-r from-primary to-primary-container text-on-primary px-5 py-3 rounded-xl font-label uppercase tracking-widest text-xs font-bold hover:opacity-95 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:transform-none"
                  >
                    Send
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
