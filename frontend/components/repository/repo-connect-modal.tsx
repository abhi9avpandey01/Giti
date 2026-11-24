'use client';
import React, { useState } from 'react';
import { api, Repository } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { X, GitPullRequest, Loader2 } from 'lucide-react';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onConnected: (repo: Repository) => void;
}

export const RepoConnectModal: React.FC<Props> = ({ isOpen, onClose, onConnected }) => {
  const [url, setUrl] = useState('');
  const [branch, setBranch] = useState('main');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setLoading(true);
    setError('');

    try {
      const repo = await api.connectRepository(url.trim(), branch.trim() || 'main');
      onConnected(repo);
      onClose();
      setUrl('');
    } catch (err: any) {
      setError(err?.message || 'Failed to connect repository. Verify the GitHub URL.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-md p-6 shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-200"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2.5 mb-4">
          <div className="p-2 bg-blue-600/10 rounded-lg text-blue-400">
            <GitPullRequest className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-100 text-lg">Connect Repository</h3>
            <p className="text-xs text-slate-400">Giti will index files and extract source embeddings</p>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-2.5 bg-red-500/10 border border-red-500/30 rounded-lg text-xs text-red-400">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              GitHub Repository URL
            </label>
            <input
              type="text"
              required
              placeholder="https://github.com/owner/repository"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              Target Branch
            </label>
            <input
              type="text"
              value={branch}
              onChange={(e) => setBranch(e.target.value)}
              placeholder="main"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex gap-2 justify-end pt-2">
            <Button type="button" variant="outline" size="sm" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" size="sm" disabled={loading || !url.trim()}>
              {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
              Connect & Index
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};
