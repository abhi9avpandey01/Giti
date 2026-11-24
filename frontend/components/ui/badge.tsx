import React from 'react';

interface BadgeProps {
  status: 'pending' | 'indexing' | 'completed' | 'failed' | string;
}

export const Badge: React.FC<BadgeProps> = ({ status }) => {
  const styles: Record<string, string> = {
    completed: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    indexing: "bg-amber-500/10 text-amber-400 border-amber-500/20 animate-pulse",
    pending: "bg-slate-500/10 text-slate-400 border-slate-500/20",
    failed: "bg-red-500/10 text-red-400 border-red-500/20",
  };

  return (
    <span className={`px-2.5 py-0.5 text-xs font-semibold rounded-full border ${styles[status] || styles.pending}`}>
      {status}
    </span>
  );
};
