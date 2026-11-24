# GITI - AI-Powered GitHub Codebase Assistant

Giti is a developer-focused AI assistant that connects directly to GitHub repositories to help software engineers, teams, and students understand architecture, debug issues, and review code using Retrieval-Augmented Generation (RAG) and agentic workflows.

## Core USP (Unique Selling Proposition)
Instead of relying on generic LLM knowledge or manual navigation through hundreds of files, Giti:
1. Indexes GitHub repositories and generates semantic vector embeddings of code chunks with file paths and line numbers preserved.
2. Uses a **LangGraph-driven RAG workflow** (Query Classifier → Repository Retriever → Context Relevance Checker → Query Rewriter → Response Generator → Source Verifier).
3. Produces **evidence-grounded answers** with exact source file and line number citations.

## Tech Stack
- **Frontend**: Next.js, React, Tailwind CSS
- **Backend**: FastAPI (Python)
- **AI / Agentic Workflow**: LangChain, LangGraph, Google Gemini API (`gemini-1.5-pro` / `gemini-1.5-flash`, `text-embedding-004`)
- **Database**: Supabase PostgreSQL + `pgvector`
- **Cache**: Redis

## Folder Structure
```
giti/
|-- frontend/
|   |-- app/
|   |   |-- login/
|   |   |-- dashboard/
|   |   |-- repository/
|   |   |-- chat/
|   |   |-- layout.tsx
|   |   |-- page.tsx
|   |-- components/
|   |   |-- ui/
|   |   |-- chat/
|   |   |-- repository/
|   |   |-- dashboard/
|   |-- lib/
|   |   |-- supabase.ts
|   |   |-- api.ts
|   |-- public/
|   |-- .env.local
|   |-- package.json
|
|-- backend/
|   |-- app/
|   |   |-- main.py
|   |   |-- config.py
|   |   |-- routes/
|   |   |   |-- auth.py
|   |   |   |-- repositories.py
|   |   |   |-- chat.py
|   |   |   |-- indexing.py
|   |   |-- services/
|   |   |   |-- github_service.py
|   |   |   |-- indexing_service.py
|   |   |   |-- retrieval_service.py
|   |   |-- ai/
|   |   |   |-- llm.py
|   |   |   |-- embeddings.py
|   |   |   |-- prompts.py
|   |   |   |-- graph.py
|   |   |-- database/
|   |   |   |-- supabase.py
|   |   |   |-- redis.py
|   |   |-- schemas/
|   |   |   |-- chat.py
|   |   |   |-- repository.py
|   |-- requirements.txt
|   |-- .env
|
|-- .gitignore
|-- README.md
```
