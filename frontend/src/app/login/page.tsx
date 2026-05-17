"use client";

import { useAuthViewModel } from '@/viewmodels/AuthViewModel';

export default function LoginPage() {
  const {
    email,
    setEmail,
    password,
    setPassword,
    error,
    loading,
    loginWithEmail,
    loginWithGoogle
  } = useAuthViewModel();

  return (
    <main className="min-h-screen flex flex-col md:flex-row overflow-hidden bg-background text-on-surface">
      {/* Left Side: Professional Illustration Space */}
      <section className="hidden md:flex md:w-1/2 lg:w-3/5 bg-surface-dim relative items-center justify-center p-12 overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img 
            className="w-full h-full object-cover opacity-90" 
            alt="A warm, professional legal consultation workspace at dusk" 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuB3JX3ZaNinswlhYw4rSvUISnb7nK8DyPZM-0YdhT28Zk0jpYouAMu_OMWpX6G6aMbIn43GwkQuY8JGMylZ5_Lvc-vK6eF4Bxz4vOYahNtrcP-mGjctOYBOA0zKEpXECtb7uzU-B7IIyXsNa3BSGgFgFRgoBegKytdNyGYqX1w00BuNYx1zVyG2ufxJDy6xVXlVrEwId59MqbVjOf0LsSFRMNbHg3gGpjRamTc3Z5q66sxQs7wFI4LgNdPDjNH74vkayDNssX_VIqU"
          />
          <div className="absolute inset-0 bg-gradient-to-tr from-surface-dim/40 to-transparent"></div>
        </div>
        {/* Branding Overlay */}
        <div className="relative z-10 max-w-md">
          <div className="mb-6">
            <span className="font-headline italic font-bold text-4xl text-surface-bright tracking-tight">LexGuard</span>
          </div>
          <h1 className="font-headline text-5xl font-bold text-surface-bright leading-tight mb-4">
            The Archive of <br/>Legal Excellence.
          </h1>
          <p className="text-surface-variant font-body text-lg leading-relaxed">
            Access high-end legal intelligence and professional curations tailored for the scholarly mind.
          </p>
        </div>
      </section>

      {/* Right Side: Login Card */}
      <section className="flex-1 flex flex-col justify-center items-center p-6 md:p-12 lg:p-24 paper-texture">
        {/* Mobile Logo (Hidden on Desktop) */}
        <div className="md:hidden mb-12 self-start">
          <span className="font-headline italic font-bold text-2xl text-on-surface">LexGuard</span>
        </div>
        
        <div className="w-full max-w-md">
          <div className="mb-10">
            <h2 className="font-headline text-3xl font-semibold text-on-surface mb-2">Welcome back</h2>
            <p className="text-on-surface-variant font-body">Welcome to your private legal advisor.</p>
          </div>

          {error && (
            <div className="mb-4 p-3 text-sm text-red-500 bg-red-50 rounded-lg border border-red-100">
              {error}
            </div>
          )}

          {/* Login Options */}
          <div className="space-y-4">
            {/* Google Login */}
            <button 
              onClick={loginWithGoogle}
              disabled={loading}
              className="w-full flex items-center justify-center gap-3 py-3 px-4 bg-surface-container-lowest hover:bg-surface-container-low transition-colors duration-200 outline-variant/15 outline outline-1 rounded-xl group disabled:opacity-50"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"></path>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"></path>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"></path>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"></path>
              </svg>
              <span className="font-label font-semibold text-sm tracking-wide text-on-surface">CONTINUE WITH GOOGLE</span>
            </button>

            <div className="relative py-4">
              <div aria-hidden="true" className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-outline-variant/30"></div>
              </div>
              <div className="relative flex justify-center text-xs">
                <span className="px-3 paper-texture text-on-surface-variant font-label tracking-widest uppercase">Or email intelligence</span>
              </div>
            </div>

            {/* Email Form */}
            <form className="space-y-6" onSubmit={(e) => { e.preventDefault(); loginWithEmail(); }}>
              <div>
                <label className="block font-label text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-2" htmlFor="email">Institutional Email</label>
                <input 
                  className="block w-full px-4 py-3 bg-surface-container-lowest border-0 ring-1 ring-outline-variant/30 focus:ring-2 focus:ring-primary rounded-xl text-on-surface transition-all" 
                  id="email" 
                  name="email" 
                  placeholder="name@lexguard.com" 
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>
              
              <div>
                <div className="flex justify-between mb-2">
                  <label className="block font-label text-xs font-semibold text-on-surface-variant uppercase tracking-wider" htmlFor="password">Access Code</label>
                  <a className="font-label text-xs text-primary hover:underline underline-offset-4 tracking-wide uppercase" href="#">Forgot?</a>
                </div>
                <input 
                  className="block w-full px-4 py-3 bg-surface-container-lowest border-0 ring-1 ring-outline-variant/30 focus:ring-2 focus:ring-primary rounded-xl text-on-surface transition-all" 
                  id="password" 
                  name="password" 
                  placeholder="••••••••" 
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <div className="flex items-center">
                <input className="h-4 w-4 text-primary focus:ring-primary border-outline-variant rounded-sm" id="remember-me" name="remember-me" type="checkbox"/>
                <label className="ml-2 block text-sm text-on-surface-variant font-body" htmlFor="remember-me">
                  Keep session active for research
                </label>
              </div>

              <button 
                disabled={loading}
                className="w-full py-4 bg-gradient-to-r from-primary to-primary-container text-on-primary font-label font-bold tracking-widest uppercase text-sm rounded-xl hover:opacity-90 transform active:scale-[0.98] transition-all duration-200 disabled:opacity-50" 
                type="submit"
              >
                Enter Archive
              </button>
            </form>
          </div>
          
          <div className="mt-10 text-center">
            <p className="text-sm text-on-surface-variant font-body">
              New to LexGuard? <a className="text-primary font-semibold hover:underline underline-offset-4" href="#">Request digital access</a>
            </p>
          </div>
        </div>

        {/* Global Footer Mirror (Simplified for Login) */}
        <footer className="mt-auto pt-12 flex flex-col items-center gap-4">
          <div className="flex gap-6">
            <a className="font-label text-[10px] uppercase tracking-[0.2em] text-on-surface-variant hover:text-primary transition-colors" href="#">Ethics</a>
            <a className="font-label text-[10px] uppercase tracking-[0.2em] text-on-surface-variant hover:text-primary transition-colors" href="#">Compliance</a>
            <a className="font-label text-[10px] uppercase tracking-[0.2em] text-on-surface-variant hover:text-primary transition-colors" href="#">Privacy</a>
          </div>
          <span className="font-label text-[10px] uppercase tracking-widest text-secondary/60">
            © 2024 LexGuard Editorial. Professional Legal Intelligence.
          </span>
        </footer>
      </section>
    </main>
  );
}
