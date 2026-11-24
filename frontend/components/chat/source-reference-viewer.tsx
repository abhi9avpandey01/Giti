'use client';
import React, { useState } from 'react';
import { SourceReference } from '@/lib/api';
import { ChevronDown, ChevronRight, FileCode } from 'lucide-react';

interface Props {
  references: SourceReference[];
}

export const SourceReferenceViewer: React.FC<Props> = ({ references }) => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  if (!references || references.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-slate-700/60">
      <p className="text-xs font-semibold text-slate-400 mb-2 flex items-center gap-1.5">
        <FileCode className="w-3.5 h-3.5 text-blue-400" />
        Verified Code References ({references.length})
      </p>
      <div className="space-y-1.5">
        {references.map((ref, idx) => {
          const isOpen = openIndex === idx;
          return (
            <div
              key={idx}
              className="text-xs bg-slate-900/60 rounded border border-slate-700/50 overflow-hidden"
            >
              <button
                onClick={() => setOpenIndex(isOpen ? null : idx)}
                className="w-full px-2.5 py-1.5 flex items-center justify-between text-left hover:bg-slate-800/50 transition-colors"
              >
                <span className="font-mono text-blue-300">
                  {ref.file_path}:{ref.start_line}-{ref.end_line}
                </span>
                {isOpen ? (
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                ) : (
                  <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
                )}
              </button>
              {isOpen && ref.snippet && (
                <pre className="p-2.5 bg-black/40 text-slate-300 font-mono text-[11px] overflow-x-auto border-t border-slate-800">
                  {ref.snippet}
                </pre>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
