import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { GitBranch, ShieldCheck, Search, Zap, ArrowRight, Code2 } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="relative overflow-hidden">
      {/* Hero Section */}
      <section className="py-24 px-4 max-w-5xl mx-auto text-center space-y-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold uppercase tracking-wider">
          <Zap className="w-3.5 h-3.5" /> LangGraph-Orchestrated Code Intelligence
        </div>

        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-white leading-tight">
          Ask questions. Get answers backed by{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">
            actual code evidence.
          </span>
        </h1>

        <p className="text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
          Giti connects to your GitHub repositories, semantically indexes functions and modules, and provides an AI codebase assistant with verified file and line citations.
        </p>

        <div className="flex flex-wrap justify-center gap-3 pt-4">
          <Link href="/dashboard">
            <Button size="lg" className="gap-2">
              Get Started with GitHub <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
          <Link href="/login">
            <Button variant="secondary" size="lg">
              Sign In
            </Button>
          </Link>
        </div>
      </section>

      {/* Feature Grid - PRD Section 13.1 */}
      <section className="py-16 border-t border-slate-900 bg-slate-950/40">
        <div className="max-w-6xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-6 bg-slate-900/60 rounded-2xl border border-slate-800">
            <Search className="w-8 h-8 text-blue-400 mb-3" />
            <h3 className="text-lg font-semibold text-white mb-2">Repository Understanding</h3>
            <p className="text-sm text-slate-400">
              Traverse architectures, modules, and cross-file dependencies in unfamiliar codebases without getting lost in hundreds of files.
            </p>
          </div>

          <div className="p-6 bg-slate-900/60 rounded-2xl border border-slate-800">
            <Code2 className="w-8 h-8 text-indigo-400 mb-3" />
            <h3 className="text-lg font-semibold text-white mb-2">Bug Investigation</h3>
            <p className="text-sm text-slate-400">
              Feed error traces or natural language bug descriptions and receive root cause analysis with targeted fix candidates.
            </p>
          </div>

          <div className="p-6 bg-slate-900/60 rounded-2xl border border-slate-800">
            <ShieldCheck className="w-8 h-8 text-emerald-400 mb-3" />
            <h3 className="text-lg font-semibold text-white mb-2">Source-Verified Evidence</h3>
            <p className="text-sm text-slate-400">
              Zero pure hallucinations. Responses are grounded in pgvector similarity retrieval and passed through an automated source verifier.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
