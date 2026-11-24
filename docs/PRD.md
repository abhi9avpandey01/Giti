# GITI - Product Requirements Document (PRD v1.0)
> **Reference File**: [docs/giti_prd.pdf](file:///d:/giti/docs/giti_prd.pdf)  
> **Status**: Initial Development  
> **Target Architecture**: Modular Monolith (FastAPI + Next.js + Supabase + Redis + LangGraph + Gemini)

---

## 1. Product Overview & USP
- **Product Name**: Giti
- **Product Type**: AI-Powered GitHub Codebase Assistant
- **USP (Unique Selling Proposition)**:
  - Repository-aware AI assistant with semantic code search.
  - Generates answers strictly grounded in actual code evidence with accurate file paths and line numbers.
  - LangGraph cyclical workflow with built-in query classification, relevance checks, query rewriter, response generation, and source verification.
  - Zero arbitrary code execution or unverified hallucinations.

---

## 2. Technology Stack
| Layer | Technology |
|---|---|
| **Frontend** | Next.js (App Router), React, Tailwind CSS |
| **Backend** | FastAPI (Python) |
| **Orchestration & RAG** | LangChain & LangGraph |
| **LLM Provider** | Google Gemini (`gemini-1.5-flash` / `gemini-1.5-pro`) |
| **Embeddings** | Gemini (`models/text-embedding-004`, 768 dimensions) |
| **Database & Vectors** | Supabase PostgreSQL with `pgvector` |
| **Caching** | Redis (Railway / Upstash / Local) |
| **Version Control & Ingestion**| GitHub REST API |
| **Hosting** | Vercel (Frontend), Railway / Render (Backend) |

---

## 3. LangGraph Workflow (Figure 6.1)
```
User Query 
    │
    ▼
Query Classifier (explanation | debug | review | general)
    │
    ▼
Repository Retriever (pgvector similarity search top_k)
    │
    ▼
Context Relevance Checker
    ├── If Relevant ──► Response Generator ──► Source Verifier ──► Final Answer
    └── If Not Relevant (max 1 retry) ──► Query Rewriter ──► Repository Retriever
```

---

## 4. Database Schema (Supabase PostgreSQL + pgvector)
1. **profiles**: `id` (UUID PK), `email` (TEXT), `created_at` (TIMESTAMP)
2. **repositories**: `id` (UUID PK), `user_id` (UUID FK), `github_url` (TEXT), `name` (TEXT), `branch` (TEXT), `commit_sha` (TEXT), `indexing_status` (TEXT), `created_at` (TIMESTAMP)
3. **code_chunks**: `id` (UUID PK), `repository_id` (UUID FK), `file_path` (TEXT), `start_line` (INT), `end_line` (INT), `content` (TEXT), `embedding` (`VECTOR(768)`), `created_at` (TIMESTAMP)
4. **conversations**: `id` (UUID PK), `user_id` (UUID FK), `repository_id` (UUID FK), `title` (TEXT), `created_at` (TIMESTAMP)
5. **messages**: `id` (UUID PK), `conversation_id` (UUID FK), `role` (`'user'` | `'assistant'`), `content` (TEXT), `created_at` (TIMESTAMP)
- **Vector RPC**: `match_code_chunks(query_embedding, match_threshold, match_count, filter_repository_id)`

---

## 5. API Endpoints
- **Auth**: `GET /api/auth/me`
- **Repositories**:
  - `GET /api/repositories`
  - `POST /api/repositories/connect`
  - `GET /api/repositories/{id}`
  - `DELETE /api/repositories/{id}`
  - `POST /api/repositories/{id}/index`
- **Chat**:
  - `POST /api/chat`
  - `GET /api/conversations`
  - `GET /api/conversations/{id}`
  - `GET /api/conversations/{id}/messages`
- **Code Analysis**:
  - `POST /api/repositories/{id}/explain`
  - `POST /api/repositories/{id}/debug`
  - `POST /api/repositories/{id}/review`
- **Indexing**:
  - `GET /api/indexing/status/{repository_id}`

---

## 6. Scope Exclusions for Initial Launch
- Docker & Kubernetes (keep setup clean, lightweight, and cloud-native).
- Autonomous code writing or pull request creation (advisory only).
- Distributed worker queues (FastAPI `BackgroundTasks` + Redis is sufficient).
