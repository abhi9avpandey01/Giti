# GITI - Production Setup & Safe Deployment Guide

Follow these sequential steps to safely set up and deploy Giti without breaking in production.

---

## Step 1: Database Setup (Supabase)
1. Log in to [Supabase Console](https://supabase.com/dashboard).
2. Create a new project named `giti-db`.
3. In the left menu, click **SQL Editor**.
4. Open the SQL script located at:
   `backend/supabase_schema.sql`
5. Copy its entire content and run it inside Supabase SQL Editor.
   - This enables the `vector` extension.
   - It creates the 5 required tables (`profiles`, `repositories`, `code_chunks`, `conversations`, `messages`).
   - It sets up vector indexes (`ivfflat` on 768-dim embeddings) and the `match_code_chunks` RPC procedure.
6. In **Settings -> API**, copy:
   - `Project URL`
   - `anon public key`
   - `service_role secret key`

---

## Step 2: Google Gemini API Setup
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Create an API Key for Gemini.
3. Verify that your project has access to `gemini-1.5-flash` and `text-embedding-004`.

---

## Step 3: Redis Cache Setup
- For cloud/production: Create a free Redis instance on [Railway](https://railway.app/) or [Upstash Redis](https://upstash.com/).
- Copy your `REDIS_URL` connection string (e.g., `rediss://default:xxxx@host:port`).

---

## Step 4: Local Testing Before Deploying
Before deploying to production, run locally to confirm zero errors:

### Backend:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
# Set your keys in backend/.env
uvicorn app.main:app --reload --port 8000
```
Visit `http://localhost:8000/docs` to inspect Swagger UI and test `/health_check` and `/api/auth/me`.

### Frontend:
```powershell
cd frontend
npm install
# Set your keys in frontend/.env.local
npm run dev
```
Visit `http://localhost:3000` to verify landing page, dashboard, and chat UI.

---

## Step 5: Safe Production Deployment

### 1. Deploy Backend (Railway or Render)
- Connect your GitHub repository to **Railway** or **Render**.
- Set the Root Directory to `backend`.
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Set Environment Variables:
  - `GEMINI_API_KEY`
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `SUPABASE_ANON_KEY`
  - `REDIS_URL`
  - `CORS_ORIGINS`: `["https://your-frontend-domain.vercel.app"]`
  - `ENVIRONMENT`: `production`

### 2. Deploy Frontend (Vercel)
- Connect repository to **Vercel**.
- Root Directory: `frontend`
- Framework Preset: `Next.js`
- Set Environment Variables:
  - `NEXT_PUBLIC_BACKEND_URL`: URL of your deployed Railway/Render backend (e.g. `https://giti-api.up.railway.app`)
  - `NEXT_PUBLIC_SUPABASE_URL`: Supabase project URL
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Supabase anon key

---

## Step 6: Production Verification Checklist
- [ ] Backend `/` returns `{"status":"healthy"}`.
- [ ] CORS in backend includes the live Vercel domain.
- [ ] Database RLS is active on Supabase.
- [ ] No API keys are committed to Git (verified via `.gitignore`).
- [ ] Supabase `match_code_chunks` RPC function returns results for vector queries.
