'use client';
import React, { useState } from 'react';
import { api, ChatMessage, SourceReference } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { SourceReferenceViewer } from './source-reference-viewer';
import { Send, Bot, User, Loader2 } from 'lucide-react';

interface Props {
  repositoryId: string;
}

export const ChatInterface: React.FC<Props> = ({ repositoryId }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input.trim();
    setInput('');

    const newMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: userText,
    };
    setMessages(prev => [...prev, newMsg]);
    setLoading(true);

    try {
      const res = await api.sendChatMessage(repositoryId, userText, conversationId);
      if (res.conversation_id) setConversationId(res.conversation_id);

      const botMsg: ChatMessage = {
        id: res.message_id || Date.now().toString(),
        role: 'assistant',
        content: res.answer,
        source_references: res.source_references,
      };
      setMessages(prev => [...prev, botMsg]);
    } catch {
      const errorMsg: ChatMessage = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Error: Unable to process query. Please check your backend connection.',
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[700px] bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center text-slate-400">
            <Bot className="w-12 h-12 mb-3 text-blue-500/80 animate-pulse" />
            <h3 className="text-base font-semibold text-slate-200">Giti Codebase Assistant</h3>
            <p className="text-xs max-w-sm mt-1 text-slate-400">
              Ask anything about the architecture, execution flow, bug investigations, or functions in this repository.
            </p>
          </div>
        ) : (
          messages.map((m) => (
            <div
              key={m.id}
              className={`flex gap-3 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {m.role === 'assistant' && (
                <div className="w-7 h-7 rounded-lg bg-blue-600 flex items-center justify-center shrink-0 mt-0.5">
                  <Bot className="w-4 h-4 text-white" />
                </div>
              )}
              <div
                className={`max-w-[80%] rounded-xl px-4 py-3 text-sm leading-relaxed ${
                  m.role === 'user'
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-slate-800/90 text-slate-100 border border-slate-700/60'
                }`}
              >
                <div className="whitespace-pre-wrap">{m.content}</div>
                {m.source_references && m.source_references.length > 0 && (
                  <SourceReferenceViewer references={m.source_references} />
                )}
              </div>
              {m.role === 'user' && (
                <div className="w-7 h-7 rounded-lg bg-slate-700 flex items-center justify-center shrink-0 mt-0.5">
                  <User className="w-4 h-4 text-slate-200" />
                </div>
              )}
            </div>
          ))
        )}
        {loading && (
          <div className="flex gap-3 items-center text-slate-400 text-xs py-2">
            <Loader2 className="w-4 h-4 animate-spin text-blue-400" />
            Retrieving relevant code and verifying source references...
          </div>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="p-3 bg-slate-950/80 border-t border-slate-800 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about this repository (e.g. 'Where is auth handled?')..."
          className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500"
        />
        <Button type="submit" disabled={loading || !input.trim()}>
          <Send className="w-4 h-4" />
        </Button>
      </form>
    </div>
  );
};
