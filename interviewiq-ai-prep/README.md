# InterviewIQ — Enhanced AI Interview Prep Platform

A full-stack SWE portfolio project for practicing technical interviews. It includes question generation, answer evaluation, saved history, analytics, timed mock interviews, project-defense mode, and a 7-day study plan generator.

## Features

- React + Vite frontend
- FastAPI backend
- SQLite saved answer history
- Many Easy/Medium/Hard questions across data structures, algorithms, system design, OOP, and debugging
- Rubric scoring: correctness, clarity, technical depth, edge cases, complexity
- Follow-up interview questions after each answer
- Progress dashboard and weakness analytics
- Timed 20-minute mock interview mode
- Resume/project defense mode
- 7-day study plan generator

## Run locally

### Backend

```bash
cd backend
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

### Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

## Interview demo script

1. Click **Load Interview Demo**.
2. Click **Generate Question** and answer it briefly.
3. Click **Evaluate Answer** and show the rubric breakdown.
4. Start a **Mock Interview** to show the timed session.
5. Click **Study Plan** to show targeted improvement suggestions.
6. Open **Saved Answer History** to show persistence.

## How to explain it

“I built a full-stack technical interview platform using React, FastAPI, and SQLite. The backend generates role-specific interview questions, evaluates answers with a rubric-based scoring engine, stores attempts, and computes weakness analytics. The frontend provides timed mock interviews, project-defense practice, progress tracking, and personalized study plans.”

## Deployment

- Frontend: Vercel
- Backend: Render
- Database: SQLite locally; PostgreSQL/Supabase for production

Set `VITE_API_BASE_URL` in Vercel to your Render backend URL.
