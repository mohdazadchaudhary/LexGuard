"use client";

import Link from "next/link";
import { useAuthViewModel } from "@/viewmodels/AuthViewModel";

export default function Home() {
  const { user, loading } = useAuthViewModel();

  return (
    <div className="min-h-screen bg-background text-on-surface font-body paper-texture flex flex-col justify-between">
      {/* Top Navbar */}
      <header className="bg-surface-container-lowest/80 backdrop-blur-md border-b border-outline-variant/15 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <span className="font-headline italic font-bold text-2xl text-primary">LexGuard</span>
            <span className="hidden sm:inline-block px-2 py-1 bg-surface-container text-on-surface-variant text-[10px] uppercase font-label tracking-widest rounded-sm">
              AI Multi-Agent System
            </span>
          </div>
          <div>
            {!loading && user ? (
              <Link
                href="/dashboard"
                className="text-xs font-label uppercase tracking-widest text-primary font-bold bg-surface-container-high hover:bg-surface-container-highest px-4 py-2.5 rounded-lg transition-all"
              >
                Go to Workspace
              </Link>
            ) : (
              <Link
                href="/login"
                className="text-xs font-label uppercase tracking-widest bg-gradient-to-r from-primary to-primary-container text-on-primary font-bold hover:opacity-90 px-4 py-2.5 rounded-lg transition-all shadow-sm"
              >
                Access Archive
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-24 flex-1 flex flex-col items-center justify-center">
        <div className="text-center max-w-3xl mb-16">
          <span className="text-xs font-label font-bold tracking-[0.25em] text-primary uppercase bg-primary/10 px-3 py-1.5 rounded-full inline-block mb-4">
            Advanced Contract Analytics
          </span>
          <h1 className="font-headline text-5xl sm:text-6xl font-bold text-on-surface tracking-tight leading-[1.15] mb-6">
            Review Contracts with <br />
            <span className="bg-gradient-to-r from-primary to-primary-container bg-clip-text text-transparent">
              Multi-Agent AI Intelligence
            </span>
          </h1>
          <p className="font-headline text-on-surface-variant text-lg leading-relaxed max-w-2xl mx-auto">
            LexGuard automatically dissects Terms of Service, NDAs, and complex contracts for legal, financial, and privacy liabilities using Google Gemini core models.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            {loading ? (
              <div className="px-8 py-4 bg-surface-container text-on-surface-variant rounded-xl font-label tracking-widest uppercase text-sm animate-pulse">
                Loading Session...
              </div>
            ) : user ? (
              <Link
                href="/dashboard"
                className="px-8 py-4 bg-gradient-to-r from-primary to-primary-container text-on-primary font-label font-bold tracking-widest uppercase text-sm rounded-xl hover:opacity-95 shadow-sm hover:scale-[1.02] hover:-translate-y-0.5 active:scale-[0.98] transition-all duration-200"
              >
                Enter Legal Workspace
              </Link>
            ) : (
              <Link
                href="/login"
                className="px-8 py-4 bg-gradient-to-r from-primary to-primary-container text-on-primary font-label font-bold tracking-widest uppercase text-sm rounded-xl hover:opacity-95 shadow-sm hover:scale-[1.02] hover:-translate-y-0.5 active:scale-[0.98] transition-all duration-200"
              >
                Start Free Risk Scan
              </Link>
            )}
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-surface-container-high hover:bg-surface-container-highest transition-all text-primary font-label font-bold tracking-widest uppercase text-sm rounded-xl flex items-center justify-center gap-2 hover:scale-[1.02] hover:-translate-y-0.5 active:scale-[0.98]"
            >
              Interactive API Docs →
            </a>
          </div>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
          {/* Card 1 */}
          <div className="bg-surface-container-lowest/70 backdrop-blur-md border border-outline-variant/15 p-8 rounded-2xl shadow-sm hover:shadow-md hover:scale-[1.02] hover:-translate-y-0.5 transition-all duration-300 ease-out">
            <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center text-primary mb-6">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="font-headline text-xl font-bold text-on-surface mb-3">Financial Risk Agent</h3>
            <p className="text-on-surface-variant text-sm leading-relaxed">
              Scrutinizes contract documents for hidden fees, auto-renewal trap doors, payment terms, and unexpected financial liabilities.
            </p>
          </div>

          {/* Card 2 */}
          <div className="bg-surface-container-lowest/70 backdrop-blur-md border border-outline-variant/15 p-8 rounded-2xl shadow-sm hover:shadow-md hover:scale-[1.02] hover:-translate-y-0.5 transition-all duration-300 ease-out">
            <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center text-primary mb-6">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
              </svg>
            </div>
            <h3 className="font-headline text-xl font-bold text-on-surface mb-3">Legal & Liability Agent</h3>
            <p className="text-on-surface-variant text-sm leading-relaxed">
              Reviews indemnification, governing jurisdiction, unilateral termination policies, and one-sided arbitration constraints.
            </p>
          </div>

          {/* Card 3 */}
          <div className="bg-surface-container-lowest/70 backdrop-blur-md border border-outline-variant/15 p-8 rounded-2xl shadow-sm hover:shadow-md hover:scale-[1.02] hover:-translate-y-0.5 transition-all duration-300 ease-out">
            <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center text-primary mb-6">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="font-headline text-xl font-bold text-on-surface mb-3">Privacy & IP Agent</h3>
            <p className="text-on-surface-variant text-sm leading-relaxed">
              Detects excessive data collection, third-party distribution rules, and unexpected intellectual property transfer terms.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-surface-container-lowest border-t border-outline-variant/15 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="flex gap-6">
            <a className="font-label text-[10px] uppercase tracking-[0.2em] text-on-surface-variant hover:text-primary transition-colors" href="#">Ethics</a>
            <a className="font-label text-[10px] uppercase tracking-[0.2em] text-on-surface-variant hover:text-primary transition-colors" href="#">Compliance</a>
            <a className="font-label text-[10px] uppercase tracking-[0.2em] text-on-surface-variant hover:text-primary transition-colors" href="#">Privacy</a>
          </div>
          <span className="font-label text-[10px] uppercase tracking-widest text-secondary/60">
            © 2024 LexGuard. Powered by Google Gemini Pro & FastAPI.
          </span>
        </div>
      </footer>
    </div>
  );
}

