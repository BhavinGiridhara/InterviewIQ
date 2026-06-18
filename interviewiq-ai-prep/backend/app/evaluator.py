import re
import uuid
from app.models import EvaluationResponse, ScoreBreakdown
from app.questions import find_question

SYNONYMS = {
    "time complexity": ["time complexity", "big o", "runtime", "o("],
    "space complexity": ["space complexity", "memory"],
    "hash map": ["hash map", "hashmap", "dictionary", "dict", "map"],
    "queue": ["queue", "fifo"],
    "stack": ["stack", "lifo"],
    "database": ["database", "db", "table", "sql"],
    "rate limiting": ["rate limit", "rate limiting", "throttle"],
    "edge case": ["edge case", "empty", "null", "duplicate", "invalid", "boundary"],
    "tradeoff": ["tradeoff", "trade-off", "however", "but", "pros", "cons"],
}

COMPLEXITY_TERMS = ["o(1", "o(n", "o(log", "o(n log", "complexity", "runtime", "space"]
EDGE_CASE_TERMS = ["edge case", "empty", "null", "none", "duplicate", "negative", "overflow", "invalid", "boundary"]
DEPTH_TERMS = ["tradeoff", "trade-off", "alternative", "because", "therefore", "however", "for example", "scales", "bottleneck"]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def concept_found(concept: str, answer: str) -> bool:
    answer_lower = normalize(answer)
    terms = SYNONYMS.get(concept.lower(), [concept.lower()])
    return any(term in answer_lower for term in terms)


def grade_from_score(score: int) -> str:
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Strong"
    if score >= 60:
        return "Developing"
    return "Needs Work"


def make_followups(question, missing: list[str], answer_clean: str) -> list[str]:
    followups = []
    if missing:
        followups.append(f"Can you explain how {missing[0]} affects your solution?")
    if not any(term in answer_clean for term in COMPLEXITY_TERMS):
        followups.append("What are the time and space complexities of your approach?")
    if not any(term in answer_clean for term in EDGE_CASE_TERMS):
        followups.append("What edge cases would you test before shipping this solution?")
    followups.append("What tradeoff would you mention if an interviewer asked for an alternative design?")
    return followups[:3]


def evaluate_answer(question_id: str, answer: str) -> EvaluationResponse:
    question = find_question(question_id)
    if not question:
        raise ValueError("Question not found.")

    answer_clean = normalize(answer)
    word_count = len(answer_clean.split())
    found = [concept for concept in question.expected_concepts if concept_found(concept, answer)]
    missing = [concept for concept in question.expected_concepts if concept not in found]

    correctness = min(40, int((len(found) / max(len(question.expected_concepts), 1)) * 40))
    clarity = 0
    if word_count >= 20:
        clarity += 8
    if word_count >= 45:
        clarity += 7
    if any(token in answer_clean for token in ["first", "then", "finally", "step"]):
        clarity += 5
    technical_depth = 0
    if any(term in answer_clean for term in DEPTH_TERMS):
        technical_depth += 10
    if len(found) >= max(2, len(question.expected_concepts) // 2):
        technical_depth += 10
    edge_cases = 10 if any(term in answer_clean for term in EDGE_CASE_TERMS) else 0
    complexity = 15 if any(term in answer_clean for term in COMPLEXITY_TERMS) else 0

    score = min(100, correctness + clarity + technical_depth + edge_cases + complexity)
    breakdown = ScoreBreakdown(
        correctness=correctness,
        clarity=clarity,
        technical_depth=technical_depth,
        edge_cases=edge_cases,
        complexity=complexity,
    )

    strengths = []
    if found:
        strengths.append("You covered important concepts: " + ", ".join(found[:6]) + ".")
    if clarity >= 15:
        strengths.append("Your answer is structured and detailed enough for an interview response.")
    if complexity:
        strengths.append("You discussed performance, which makes the answer more interview-ready.")
    if edge_cases:
        strengths.append("You mentioned edge cases, which shows engineering maturity.")
    if not strengths:
        strengths.append("You attempted the question, but the answer needs more technical detail and structure.")

    if missing:
        feedback = "Your answer is on the right track, but it should mention: " + ", ".join(missing[:6]) + "."
    elif score >= 85:
        feedback = "Strong interview answer. You covered the core concepts and added enough detail to sound confident."
    else:
        feedback = "Good start. To improve, add a clearer step-by-step explanation, complexity, tradeoffs, and edge cases."

    improved_answer = (
        "A strong answer would start by restating the problem, then explain the core approach step by step. "
        f"For this question, include {', '.join(question.expected_concepts[:6])}. "
        "Then analyze time and space complexity, mention edge cases, and close with one tradeoff or alternative."
    )

    next_steps = []
    if missing:
        next_steps.append("Review: " + ", ".join(missing[:4]) + ".")
    if not complexity:
        next_steps.append("Add Big-O time and space complexity to your next answer.")
    if not edge_cases:
        next_steps.append("Mention at least two edge cases next time.")
    next_steps.append("Practice giving this answer out loud in 60-90 seconds.")

    return EvaluationResponse(
        id=str(uuid.uuid4())[:8],
        question_id=question_id,
        score=score,
        grade=grade_from_score(score),
        breakdown=breakdown,
        strengths=strengths,
        missing_concepts=missing,
        feedback=feedback,
        improved_answer=improved_answer,
        follow_up_questions=make_followups(question, missing, answer_clean),
        next_steps=next_steps,
    )
