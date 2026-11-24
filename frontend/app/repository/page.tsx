'use client';
import React, { Suspense, useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { api, Repository } from '@/lib/api';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import { GitBranch, RefreshCw, MessageSquare, ExternalLink } from 'lucide-react';

function RepositoryDetailContent() {
  const searchParams = useSearchParams();
  const repoId = searchParams.get('id');
  const [repo, setRepo] = useState<Repository | null>(null);
  const [reindexing, setReindexing] = useState(false);

  useEffect(() => {
    if (repoId) {
      api.getRepository(repoId).then((r) => setRepo(r));
    }
  }, [repoId]);

  const handleReindex = async () => {
    if (!repo) return;
    setReindexing(true);
    await api.triggerIndexing(repo.id);
    setReindexing(false);
  };

  if (!repo) {
    return <div className="text-slate-400 p-8">Loading repository details...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-white">{repo.name}</h1>
          <Badge status={repo.indexing_status} />
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm text-slate-300">
          <div>
            <span className="text-slate-500 block text-xs">Branch</span>
            <span className="font-mono">{repo.branch}</span>
          </div>
          <div>
            <span className="text-slate-500 block text-xs">Commit SHA</span>
            <span className="font-mono text-xs">{repo.commit_sha || 'N/A'}</span>
          </div>
        </div>

        <div className="flex gap-3 pt-4 border-t border-slate-800">
          <Link href={`/chat?repo=${repo.id}`}>
            <Button className="gap-2">
              <MessageSquare className="w-4 h-4" /> Start Conversation
            </Button>
          </Link>
          <Button variant="secondary" onClick={handleReindex} disabled={reindexing} className="gap-2">
            <RefreshCw className={`w-4 h-4 ${reindexing ? 'animate-spin' : ''}`} /> Re-index Codebase
          </Button>
          <a href={repo.github_url} target="_blank" rel="noopener noreferrer">
            <Button variant="outline" className="gap-2">
              <ExternalLink className="w-4 h-4" /> View on GitHub
            </Button>
          </a>
        </div>
      </div>
    </div>
  );
}

export default function RepositoryPage() {
  return (
    <Suspense fallback={<div className="p-8 text-slate-400">Loading...</div>}>
      <RepositoryDetailContent />
    </Suspense>
  );
}
