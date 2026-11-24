'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Github, Mail } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');

  const handleGitHubLogin = () => {
    // Navigate to dashboard for dev / Supabase Auth OAuth flow
    router.push('/dashboard');
  };

  const handleEmailSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    router.push('/dashboard');
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-sm p-8 shadow-2xl space-y-6">
        <div className="text-center space-y-1">
          <h2 className="text-2xl font-bold text-white">Welcome to Giti</h2>
          <p className="text-xs text-slate-400">Sign in to connect and query your repositories</p>
        </div>

        <Button onClick={handleGitHubLogin} className="w-full gap-2 bg-slate-800 hover:bg-slate-700 text-white border border-slate-700">
          <Github className="w-4 h-4" />
          Continue with GitHub
        </Button>

        <div className="relative flex items-center justify-center">
          <div className="border-t border-slate-800 w-full" />
          <span className="bg-slate-900 px-2 text-[11px] text-slate-500 uppercase tracking-wider absolute">
            or
          </span>
        </div>

        <form onSubmit={handleEmailSubmit} className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@company.com"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>
          <Button type="submit" className="w-full">
            Sign In with Email
          </Button>
        </form>
      </div>
    </div>
  );
}
