import sqlite3
from datetime import datetime
from pathlib import Path
from app.models import EvaluationResponse
from app.questions import find_question

DB_PATH = Path(__file__).resolve().parents[2] / "interviewiq.db"


def connect():
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id TEXT PRIMARY KEY,
                candidate_name TEXT,
                question_id TEXT,
                role TEXT,
                topic TEXT,
                difficulty TEXT,
                question TEXT,
                answer TEXT,
                score INTEGER,
                grade TEXT,
                correctness INTEGER,
                clarity INTEGER,
                technical_depth INTEGER,
                edge_cases INTEGER,
                complexity INTEGER,
                feedback TEXT,
                missing_concepts TEXT,
                created_at TEXT
            )
        """)
        # Existing users from older version may have an older table. Add missing columns safely.
        existing = {row[1] for row in conn.execute("PRAGMA table_info(attempts)").fetchall()}
        for name, ddl_type in {
            "correctness": "INTEGER",
            "clarity": "INTEGER",
            "technical_depth": "INTEGER",
            "edge_cases": "INTEGER",
            "complexity": "INTEGER",
            "feedback": "TEXT",
        }.items():
            if name not in existing:
                conn.execute(f"ALTER TABLE attempts ADD COLUMN {name} {ddl_type}")


def save_attempt(candidate_name: str, question_id: str, answer: str, evaluation: EvaluationResponse) -> None:
    question = find_question(question_id)
    if not question:
        return
    with connect() as conn:
        conn.execute("""
            INSERT INTO attempts (
                id, candidate_name, question_id, role, topic, difficulty, question, answer,
                score, grade, correctness, clarity, technical_depth, edge_cases, complexity,
                feedback, missing_concepts, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            evaluation.id, candidate_name, question_id, question.role, question.topic, question.difficulty,
            question.question, answer, evaluation.score, evaluation.grade, evaluation.breakdown.correctness,
            evaluation.breakdown.clarity, evaluation.breakdown.technical_depth, evaluation.breakdown.edge_cases,
            evaluation.breakdown.complexity, evaluation.feedback, ", ".join(evaluation.missing_concepts),
            datetime.utcnow().isoformat(timespec="seconds") + "Z",
        ))


def list_attempts(limit: int = 50) -> list[dict]:
    with connect() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT id, candidate_name, role, topic, difficulty, question, answer, score, grade,
                   correctness, clarity, technical_depth, edge_cases, complexity, feedback,
                   missing_concepts, created_at
            FROM attempts ORDER BY created_at DESC LIMIT ?
        """, (limit,)).fetchall()
        return [dict(row) for row in rows]


def analytics() -> dict:
    with connect() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT topic, difficulty, score, correctness, clarity, technical_depth, edge_cases, complexity FROM attempts").fetchall()
    if not rows:
        return {
            "total_attempts": 0,
            "average_score": 0,
            "strongest_topic": None,
            "weakest_topic": None,
            "topic_scores": {},
            "recommendations": ["Complete your first practice attempt to unlock analytics."],
        }
    buckets: dict[str, list[int]] = {}
    scores = []
    rubric_totals = {"correctness": [], "clarity": [], "technical_depth": [], "edge_cases": [], "complexity": []}
    for row in rows:
        buckets.setdefault(row["topic"], []).append(row["score"])
        scores.append(row["score"])
        for key in rubric_totals:
            if row[key] is not None:
                rubric_totals[key].append(row[key])
    topic_scores = {topic: round(sum(values) / len(values), 1) for topic, values in buckets.items()}
    strongest = max(topic_scores, key=topic_scores.get)
    weakest = min(topic_scores, key=topic_scores.get)
    weakest_rubric = min(
        (key for key, values in rubric_totals.items() if values),
        key=lambda key: sum(rubric_totals[key]) / len(rubric_totals[key]),
        default="technical_depth",
    )
    return {
        "total_attempts": len(scores),
        "average_score": round(sum(scores) / len(scores), 1),
        "strongest_topic": strongest,
        "weakest_topic": weakest,
        "topic_scores": topic_scores,
        "recommendations": [
            f"Focus next on {weakest}; it is currently your lowest-scoring topic.",
            f"Your lowest rubric area is {weakest_rubric.replace('_', ' ')}. Target that in your next answers.",
            "Retake questions where you scored under 75 and compare your new answer.",
            "For every answer, include approach, complexity, tradeoffs, and edge cases.",
        ],
    }
