import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Giti - AI-Powered GitHub Codebase Assistant',
  description: 'Evidence-based codebase exploration, debugging, and code reviews using LangGraph & Gemini RAG.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased selection:bg-blue-600 selection:text-white">
        <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur sticky top-0 z-40">
          <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" className="flex items-center gap-2.5 font-bold text-lg text-white">
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center font-black text-sm tracking-tighter">
                G
              </div>
              <span>GITI</span>
            </a>
            <nav className="flex items-center gap-6 text-sm">
              <a href="/dashboard" className="text-slate-300 hover:text-white transition-colors">
                Dashboard
              </a>
              <a href="/login" className="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors">
                Sign In
              </a>
            </nav>
          </div>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
