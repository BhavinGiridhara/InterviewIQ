# InterviewIQ

Practice technical interviews, review structured feedback, and turn saved answers into a focused study plan.

InterviewIQ is a portfolio application with a React/Vite interface, a FastAPI backend, and local SQLite storage. It includes a curated technical question bank, timed mock interviews, resume project prompts, answer evaluation, progress analytics, and a history-based study plan.

> **Evaluation is rule-based.** The current backend checks expected concepts and answer signals such as structure, edge cases, and complexity. It does not call an LLM or verify whether an answer is factually correct. Scores are practice feedback, not an authoritative assessment.

## Try it

[Open the frontend demo](https://interview-iq-eight-gamma.vercel.app) · [Explore the source](interviewiq-ai-prep/)

For a complete local experience, run the backend as described below. The frontend calls the URL in `VITE_API_BASE_URL`, defaulting to `http://127.0.0.1:8000`.

## What it does

| Feature | How it works |
| --- | --- |
| Question practice | Choose a role, topic, and difficulty from a curated question bank. |
| Answer feedback | Score answers across correctness (40), clarity (20), technical depth (20), edge cases (10), and complexity (15); show missed concepts, suggestions, and follow-up questions. |
| Saved history | Persist evaluated question-bank answers in SQLite for later review. |
| Analytics | Show aggregate scores, topic strengths and weaknesses, and next-step suggestions across saved attempts. |
| Study plan | Use the latest saved attempt per question to prioritize weaker topics and produce a plan of up to seven days with concrete review tasks. |
| Mock interview | Generate a timed, 20-minute set of questions across technical topics. |
| Project defense | Generate a prompt from a project description and evaluate the response with the reusable rubric. |

The rubric's category maxima total 105, while the final score is capped at 100. Feedback uses keyword and heuristic matching; it can reward terms without fully understanding the reasoning behind them.

## Architecture

| Step | Component | What happens |
| --- | --- | --- |
| 1 | React + Vite | The candidate selects a question and submits an answer. |
| 2 | FastAPI | The API receives the request and routes it to the question bank or evaluator. |
| 3 | Evaluator | A rule-based rubric scores the answer and returns feedback. |
| 4 | SQLite | Supported attempts are saved for history and analytics. |
| 5 | Study plan | The backend reads saved attempts to suggest targeted practice. |

A candidate chooses a question and submits an answer in the browser. FastAPI evaluates it against the question's expected concepts, returns a rubric breakdown, and saves supported attempts to SQLite. The history powers the analytics and personalized study plan.

| Location | Responsibility |
| --- | --- |
| [`frontend/src/App.jsx`](interviewiq-ai-prep/frontend/src/App.jsx) | Main practice and mock interview interface |
| [`frontend/src/api/client.js`](interviewiq-ai-prep/frontend/src/api/client.js) | Frontend HTTP calls and API base URL |
| [`backend/app/main.py`](interviewiq-ai-prep/backend/app/main.py) | FastAPI routes and request flow |
| [`backend/app/questions.py`](interviewiq-ai-prep/backend/app/questions.py) | Curated questions and selection |
| [`backend/app/evaluator.py`](interviewiq-ai-prep/backend/app/evaluator.py) | Rule-based rubric and feedback |
| [`backend/app/db/repository.py`](interviewiq-ai-prep/backend/app/db/repository.py) | SQLite storage, history, and analytics |
| [`backend/app/study_plan.py`](interviewiq-ai-prep/backend/app/study_plan.py) | History-based review schedule |

## Run locally

Prerequisites: Python 3.11+, Node.js and npm. Commands below start at the repository root.

**Backend** (terminal 1):

```bash
cd interviewiq-ai-prep/backend
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`; interactive API docs are at [`/docs`](http://127.0.0.1:8000/docs). SQLite creates `backend/interviewiq.db` on startup.

**Frontend** (terminal 2, from the repository root):

```bash
cd interviewiq-ai-prep/frontend
npm install
npm run dev
```

Open `http://localhost:5173`. If your backend uses another address, set `VITE_API_BASE_URL` in the frontend environment before starting Vite.

**Docker alternative** (from the repository root):

```bash
cd interviewiq-ai-prep
docker compose up --build
```

The frontend and backend use ports 5173 and 8000 respectively. The Compose file bind-mounts the backend directory, so the local SQLite file remains in that directory.

## API overview

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/options` | Available roles, topics, difficulties, and modes |
| POST | `/api/question` | Choose a question or generate a project-defense prompt |
| POST | `/api/evaluate` | Evaluate an answer; save question-bank attempts |
| GET | `/api/history` | Latest 500 active attempts for a candidate |
| GET | `/api/analytics` | Analytics for a candidate’s active attempts |
| POST | `/api/study-plan` | Study plan for a candidate name |
| POST | `/api/mock-interview` | Timed question set |

See [FastAPI's interactive docs](http://127.0.0.1:8000/docs) for request and response schemas while the backend is running.

## Study plan and data boundaries

The planner reads saved attempts for the entered candidate name. For each question it uses the latest answer, groups performance by topic, gives more attention to lower-scoring topics, and includes saved feedback and missed concepts in daily tasks. With no saved answers for that name, it asks the candidate to practice first. Repeating the request against unchanged history produces the same plan.

Candidate names select histories; they do **not** authenticate users. History and analytics are filtered by candidate name. These names are not authenticated accounts: this remains a shared portfolio prototype, not a private multi-user service. Project-defense prompts use generated IDs and their answers are evaluated but **not saved**, so they do not affect history or the plan.

## Verify

Run the existing study-plan tests from `interviewiq-ai-prep/backend`:

```bash
python -m unittest discover -s tests
```

For a quick product walkthrough: load the interview demo, generate and evaluate a question, inspect the rubric, try a mock interview, then open history and regenerate the study plan.

## Next steps

- Add accounts and authorization, and scope history and analytics to the signed-in user.
- Save project-defense attempts so their feedback can inform the study plan.
- Improve evaluation beyond keyword matching and calibrate rubric scores.
- Use a production database such as PostgreSQL for a concurrent deployment.

## Sessions, samples and history controls

New Session clears the current draft without erasing saved practice. Sample answers use a preview endpoint and do not count toward progress. History supports topic, score and UTC-date filters, confirmed removal/reset, and Undo for the latest removal while the page stays open. See [deployment and data behavior](interviewiq-ai-prep/DEPLOY_HISTORY.md) before updating the AWS frontend.
