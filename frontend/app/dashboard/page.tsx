'use client';
import React, { useEffect, useState } from 'react';
import { api, Repository } from '@/lib/api';
import { DashboardOverview } from '@/components/dashboard/dashboard-overview';
import { RepoConnectModal } from '@/components/repository/repo-connect-modal';

export default function DashboardPage() {
  const [repos, setRepos] = useState<Repository[]>([]);
  const [modalOpen, setModalOpen] = useState(false);

  const fetchRepos = async () => {
    const list = await api.getRepositories();
    setRepos(list);
  };

  useEffect(() => {
    fetchRepos();
  }, []);

  const handleConnected = (newRepo: Repository) => {
    setRepos((prev) => [newRepo, ...prev]);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <DashboardOverview
        repositories={repos}
        onOpenConnectModal={() => setModalOpen(true)}
      />
      <RepoConnectModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        onConnected={handleConnected}
      />
    </div>
  );
}
