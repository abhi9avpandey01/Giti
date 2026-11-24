-- ==============================================================================
-- GITI Database Schema (Supabase PostgreSQL + pgvector)
-- PRD Section 7: Database Design
-- ==============================================================================

-- 1. Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Profiles Table (Section 7.2)
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Repositories Table (Section 7.3)
CREATE TABLE IF NOT EXISTS repositories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    github_url TEXT NOT NULL,
    name TEXT NOT NULL,
    branch TEXT DEFAULT 'main' NOT NULL,
    commit_sha TEXT,
    indexing_status TEXT DEFAULT 'pending' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Code Chunks Table (Section 7.4) - 768 dimensions for Gemini text-embedding-004
CREATE TABLE IF NOT EXISTS code_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repository_id UUID NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    start_line INTEGER NOT NULL,
    end_line INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(768),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 5. Conversations Table (Section 7.5)
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    repository_id UUID NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 6. Messages Table (Section 7.6)
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_repositories_user_id ON repositories(user_id);
CREATE INDEX IF NOT EXISTS idx_code_chunks_repo_id ON code_chunks(repository_id);
CREATE INDEX IF NOT EXISTS idx_conversations_user_repo ON conversations(user_id, repository_id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);

-- Vector Cosine Similarity Index (IVFFlat)
CREATE INDEX IF NOT EXISTS idx_code_chunks_embedding 
ON code_chunks USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Vector Search RPC function for Giti Retrieval
CREATE OR REPLACE FUNCTION match_code_chunks(
    query_embedding VECTOR(768),
    match_threshold FLOAT,
    match_count INT,
    filter_repository_id UUID
)
RETURNS TABLE (
    id UUID,
    repository_id UUID,
    file_path TEXT,
    start_line INT,
    end_line INT,
    content TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        cc.id,
        cc.repository_id,
        cc.file_path,
        cc.start_line,
        cc.end_line,
        cc.content,
        1 - (cc.embedding <=> query_embedding) AS similarity
    FROM code_chunks cc
    WHERE cc.repository_id = filter_repository_id
      AND 1 - (cc.embedding <=> query_embedding) > match_threshold
    ORDER BY similarity DESC
    LIMIT match_count;
END;
$$;

-- Enable Row Level Security (RLS) - PRD Section 7.7
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE repositories ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
