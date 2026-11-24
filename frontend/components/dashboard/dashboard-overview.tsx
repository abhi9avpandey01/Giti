import React from 'react';
import Link from 'next/link';
import { Repository } from '@/lib/api';
import { RepoCard } from '@/components/repository/repo-card';
import { Button } from '@/components/ui/button';
import { Plus, FolderGit2, MessageSquareCode } from 'lucide-react';

interface Props {
  repositories: Repository[];
  onOpenConnectModal: () => void;
}

export const DashboardOverview: React.FC<Props> = ({ repositories, onOpenConnectModal }) => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Repositories</h1>
          <p className="text-sm text-slate-400">Manage and chat with your connected codebases</p>
        </div>
        <Button onClick={onOpenConnectModal} className="gap-2">
          <Plus className="w-4 h-4" />
          Connect Repository
        </Button>
      </div>

      {repositories.length === 0 ? (
        <div className="bg-slate-900 border border-dashed border-slate-800 rounded-2xl p-12 text-center">
          <FolderGit2 className="w-12 h-12 text-slate-500 mx-auto mb-3" />
          <h3 className="text-base font-semibold text-slate-200">No repositories connected yet</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1 mb-4">
            Connect any public or authorized private GitHub repository to start asking questions with verified source references.
          </p>
          <Button onClick={onOpenConnectModal} size="sm">
            Connect First Repository
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {repositories.map((repo) => (
            <RepoCard key={repo.id} repo={repo} />
          ))}
        </div>
      )}
    </div>
  );
};
