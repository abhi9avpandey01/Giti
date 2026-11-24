import React from 'react';
import Link from 'next/link';
import { Repository } from '@/lib/api';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { GitBranch, MessageSquare, ExternalLink } from 'lucide-react';

interface Props {
  repo: Repository;
}

export const RepoCard: React.FC<Props> = ({ repo }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-all flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between gap-3 mb-2">
          <h3 className="font-semibold text-slate-100 text-base truncate">{repo.name}</h3>
          <Badge status={repo.indexing_status} />
        </div>
        <p className="text-xs text-slate-400 flex items-center gap-1.5 mb-4">
          <GitBranch className="w-3.5 h-3.5 text-slate-500" />
          Branch: <span className="font-mono text-slate-300">{repo.branch}</span>
          {repo.commit_sha && (
            <span className="font-mono text-[10px] text-slate-500 ml-1">
              ({repo.commit_sha.slice(0, 7)})
            </span>
          )}
        </p>
      </div>

      <div className="flex items-center gap-2 pt-3 border-t border-slate-800/80">
        <Link href={`/chat?repo=${repo.id}`} className="flex-1">
          <Button variant="primary" size="sm" className="w-full gap-1.5">
            <MessageSquare className="w-3.5 h-3.5" />
            Chat
          </Button>
        </Link>
        <a
          href={repo.github_url}
          target="_blank"
          rel="noopener noreferrer"
          className="p-2 text-slate-400 hover:text-slate-200 border border-slate-800 rounded-lg hover:border-slate-700 transition-colors"
        >
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>
    </div>
  );
};
