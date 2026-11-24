'use client';
import React, { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { ChatInterface } from '@/components/chat/chat-interface';

function ChatContent() {
  const searchParams = useSearchParams();
  const repoId = searchParams.get('repo') || 'default-repo-id';

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Repository AI Assistant</h1>
          <p className="text-xs text-slate-400">Ask architectural, debugging, or code review questions</p>
        </div>
      </div>
      <ChatInterface repositoryId={repoId} />
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="p-8 text-slate-400">Loading Chat...</div>}>
      <ChatContent />
    </Suspense>
  );
}
