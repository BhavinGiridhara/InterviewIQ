import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db.repository import analytics, init_db, list_attempts, save_attempt
from app.evaluator import evaluate_answer
from app.models import EvaluationRequest, MockInterviewRequest, QuestionRequest, StudyPlanRequest, StudyPlanResponse, StudyDay
from app.questions import QUESTION_BANK, select_question

app = FastAPI(title="InterviewIQ API", version="2.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup() -> None:
    init_db()

@app.get("/")
def root():
    return {"message": "InterviewIQ API is running.", "version": "2.0.0"}

@app.get("/api/options")
def get_options():
    return {
        "roles": sorted({q.role for q in QUESTION_BANK} | {"SWE Intern", "Backend Intern", "Frontend Intern"}),
        "topics": sorted({q.topic for q in QUESTION_BANK} | {"Resume Project Defense", "Behavioral"}),
        "difficulties": ["Easy", "Medium", "Hard"],
        "modes": ["Technical Concepts", "Timed Mock Interview", "Resume Project Defense", "Behavioral"],
    }

@app.post("/api/question")
def generate_question(request: QuestionRequest):
    if request.mode == "Resume Project Defense" or request.topic == "Resume Project Defense":
        desc = (request.project_description or "a full-stack software project").strip()
        return {
            "id": "project-defense-" + str(uuid.uuid4())[:8],
            "role": request.role,
            "topic": "Resume Project Defense",
            "difficulty": request.difficulty,
            "question": f"You listed this project: '{desc}'. Explain the problem it solves, your technical architecture, and one tradeoff you made.",
            "expected_concepts": ["problem", "architecture", "backend", "frontend", "database", "tradeoff", "impact"],
            "hints": ["Start with the user problem.", "Mention frontend, backend, and data flow.", "End with tradeoffs and future improvements."],
        }
    return select_question(request.role, request.topic, request.difficulty, request.exclude_ids)

@app.post("/api/evaluate")
def evaluate(request: EvaluationRequest):
    try:
        result = evaluate_answer(request.question_id, request.answer)
        save_attempt(request.candidate_name or "Demo User", request.question_id, request.answer, result)
        return result
    except ValueError as exc:
        # Dynamic project-defense questions are not in the static bank. Evaluate them with a reusable rubric.
        if request.question_id.startswith("project-defense-"):
            fake_question_id = "sys-api-medium"
            result = evaluate_answer(fake_question_id, request.answer)
            result.question_id = request.question_id
            return result
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.get("/api/history")
def history():
    return list_attempts()

@app.get("/api/analytics")
def get_analytics():
    return analytics()

@app.post("/api/study-plan")
def study_plan(request: StudyPlanRequest):
    data = analytics()
    focus = data.get("weakest_topic") or "Data Structures"
    recs = data.get("recommendations", [])
    days = []
    topics = [focus, "Complexity Analysis", "Data Structures", "Algorithms", "System Design", "Project Defense", "Mock Interview"]
    for i in range(1, request.days + 1):
        topic = topics[(i - 1) % len(topics)]
        days.append(StudyDay(day=i, focus=topic, tasks=[
            f"Answer 3 {topic} questions.",
            "For each answer, include approach, complexity, tradeoffs, and edge cases.",
            "Rewrite your weakest answer using the improved-answer template.",
        ]))
    return StudyPlanResponse(summary=f"Based on your history, start by improving {focus}. " + (recs[0] if recs else "Keep practicing consistently."), days=days)

@app.post("/api/mock-interview")
def mock_interview(request: MockInterviewRequest):
    selected = []
    exclude = []
    topics = ["Data Structures", "Algorithms", "System Design", "OOP", "Debugging"]
    for i in range(request.question_count):
        topic = topics[i % len(topics)]
        try:
            q = select_question(request.role, topic, request.difficulty, exclude)
        except Exception:
            q = select_question("SWE Intern", topic, request.difficulty, exclude)
        selected.append(q)
        exclude.append(q.id)
    return {"session_id": str(uuid.uuid4())[:8], "time_limit_minutes": 20, "questions": selected}
