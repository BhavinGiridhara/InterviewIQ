# Deploy practice history controls

Deploy the backend before the frontend: demo previews need the new `/api/evaluate-preview` endpoint.

## Backend (on the machine running FastAPI)

1. Back up the active `interviewiq.db` before updating. Keep the existing database location and mounted volumes.
2. Pull the latest repository and install `backend/requirements.txt` in the existing Python environment.
3. Restart the existing backend service. Startup adds the nullable `deleted_batch` column without deleting saved attempts.
4. If using this repository's Docker Compose setup, from `interviewiq-ai-prep` run `docker compose up -d --build backend`. If using systemd or another process manager, restart that existing service instead.
5. Check `/api/history?candidate_name=Demo%20User` and `/api/analytics?candidate_name=Demo%20User`.

## Frontend (PowerShell)

```powershell
cd C:\WINDOWS\system32\InterviewIQ\interviewiq-ai-prep\frontend
git pull --ff-only
$env:VITE_API_BASE_URL = "http://54.172.43.218:8000"
npm run build
aws s3 sync dist/ s3://bhavin-interviewiq-frontend/
```

## Behavior

- New Session clears the current draft, question, timer and feedback; it does not remove saved attempts. Unsaved answers prompt before clearing.
- Sample answers use a preview-only API and never contribute to history, analytics or study plans. Editing a sample keeps it in demo mode.
- History, scores and study plans follow the selected candidate name. Names are shared profile labels, **not authentication or private accounts**.
- Topic, score and UTC-date filters apply to the latest 500 visible attempts.
- Delete and Reset require confirmation. Reset applies to every active attempt for that name, regardless of the filters or 500-row display limit.
- Removal archives rows. Undo restores the most recent removal batch during the current page session. After reloading, archived rows remain in SQLite but the UI Undo option is gone.
- No existing live data is deleted by installing this update. Existing sample submissions cannot reliably be distinguished from genuine answers; remove them manually if desired.

Tests: `python -m unittest discover -s tests` from `backend`.
