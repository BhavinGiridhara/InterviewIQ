import re
import uuid
from app.models import ConceptFeedback, EvaluationResponse, ScoreBreakdown
from app.questions import find_question

SYNONYMS = {
    "time complexity": ["time complexity", "big o", "runtime", "o(", "o of", "linear", "constant", "logarithmic"],
    "space complexity": ["space complexity", "memory", "extra space", "auxiliary space"],
    "hash map": ["hash map", "hashmap", "dictionary", "dict", "map", "lookup table"],
    "hash function": ["hash function", "hash", "hashed", "hashing"],
    "key": ["key"],
    "value": ["value"],
    "bucket": ["bucket", "slot", "index"],
    "collision": ["collision", "collide", "chaining", "open addressing", "probing"],
    "queue": ["queue", "fifo", "enqueue", "dequeue"],
    "stack": ["stack", "lifo", "push", "pop"],
    "database": ["database", "db", "table", "sql", "sqlite", "postgres"],
    "backend": ["backend", "api", "server", "fastapi", "endpoint"],
    "frontend": ["frontend", "ui", "react", "client"],
    "architecture": ["architecture", "data flow", "system design", "components", "frontend", "backend", "database"],
    "problem": ["problem", "user", "pain point", "need", "solves"],
    "impact": ["impact", "useful", "helps", "benefit", "improves"],
    "rate limiting": ["rate limit", "rate limiting", "throttle"],
    "edge case": ["edge case", "empty", "null", "none", "duplicate", "invalid", "boundary", "corner case"],
    "tradeoff": ["tradeoff", "trade-off", "however", "but", "pros", "cons", "alternative", "downside"],
    "O(1)": ["o(1", "constant time", "constant lookup"],
    "O(n)": ["o(n", "linear"],
    "O(log n)": ["o(log", "logarithmic"],
}

CONCEPT_EXPLANATIONS = {
    "time complexity": ("Interviewers expect runtime because it proves you understand how the solution scales.", "Add a sentence like: 'The time complexity is O(n) because we scan the input once.'"),
    "space complexity": ("Space complexity shows whether your solution uses extra memory responsibly.", "Add: 'The space complexity is O(n) for the hash map / stack / visited set.'"),
    "hash map": ("A hash map is often the core optimization that avoids brute force.", "Say what the map stores, such as value-to-index, key-to-count, or node-to-state."),
    "hash function": ("Hashing is the reason average lookup can be constant time.", "Explain that the key is converted into an index/bucket using a hash function."),
    "collision": ("Collisions are the main caveat behind hash table performance.", "Mention chaining or open addressing and that worst case can degrade if many keys collide."),
    "bucket": ("Buckets explain where hashed keys actually land internally.", "Say that a hash table places keys into buckets/slots based on the hash."),
    "queue": ("The queue behavior matters because FIFO order affects the algorithm design.", "Explicitly say enqueue/dequeue and how FIFO changes the implementation."),
    "stack": ("Stack behavior matters because LIFO order is usually the reason the structure is chosen.", "Mention push/pop and why last-in-first-out is useful here."),
    "tradeoff": ("Tradeoffs make your answer sound like engineering, not memorization.", "Compare two options and state what becomes faster, slower, simpler, or more memory-heavy."),
    "edge case": ("Edge cases show that you can move from theory to production-quality code.", "Name at least two tests: empty input, one item, duplicates, null/invalid input, or capacity limits."),
    "architecture": ("Architecture shows you understand how the full system fits together.", "Describe frontend, backend, database, and request/response flow."),
    "backend": ("Backend details show your personal technical contribution beyond the UI.", "Mention APIs, validation, persistence, routing, authentication, or business logic."),
    "frontend": ("Frontend details show how users interact with the product.", "Mention React components, state management, form flow, or UI feedback."),
    "database": ("Database choices matter because they affect persistence and future scaling.", "Say what data you store, why you chose SQLite/PostgreSQL, and how you would scale it."),
    "problem": ("Interviewers want to hear the problem before the technology.", "Start with: 'This solves X problem for Y users by doing Z.'"),
    "impact": ("Impact explains why the project matters beyond being a coding exercise.", "Add a measurable or user-focused benefit, such as faster prep, clearer feedback, or tracked improvement."),
}

COMPLEXITY_TERMS = ["o(1", "o(n", "o(log", "o(n log", "complexity", "runtime", "space", "constant", "linear", "logarithmic"]
EDGE_CASE_TERMS = ["edge case", "empty", "null", "none", "duplicate", "negative", "overflow", "invalid", "boundary", "one element", "corner case"]
DEPTH_TERMS = ["tradeoff", "trade-off", "alternative", "because", "therefore", "however", "for example", "scales", "bottleneck", "drawback", "downside"]
STRUCTURE_TERMS = ["first", "then", "finally", "step", "approach", "after that", "next"]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def concept_found(concept: str, answer: str) -> bool:
    answer_lower = normalize(answer)
    terms = SYNONYMS.get(concept.lower(), [concept.lower()])
    return any(term.lower() in answer_lower for term in terms)


def grade_from_score(score: int) -> str:
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Strong"
    if score >= 60:
        return "Developing"
    return "Needs Work"


def explain_concept(concept: str) -> tuple[str, str]:
    lowered = concept.lower()
    if lowered in CONCEPT_EXPLANATIONS:
        return CONCEPT_EXPLANATIONS[lowered]
    return (
        f"'{concept}' is one of the expected ideas for this question, so leaving it out makes the answer feel incomplete.",
        f"Add one clear sentence explaining {concept} and connect it directly to your solution."
    )


def make_concept_feedback(expected: list[str], found: list[str], missing: list[str]) -> list[ConceptFeedback]:
    cards: list[ConceptFeedback] = []
    found_set = set(found)
    missing_set = set(missing)
    for concept in expected[:10]:
        why, how = explain_concept(concept)
        status = "covered" if concept in found_set else "missing" if concept in missing_set else "not checked"
        cards.append(ConceptFeedback(concept=concept, status=status, why_it_matters=why, how_to_add_it=how))
    return cards


def make_answer_gaps(answer_clean: str, missing: list[str], word_count: int) -> list[str]:
    gaps = []
    if word_count < 35:
        gaps.append("Your answer is too short for an interview. It needs an approach, reasoning, complexity, and at least one example or edge case.")
    if missing:
        gaps.append("You did not mention these expected concepts: " + ", ".join(missing[:6]) + ".")
    if not any(term in answer_clean for term in COMPLEXITY_TERMS):
        gaps.append("You did not give time or space complexity. Interviewers usually expect Big-O analysis for technical questions.")
    if not any(term in answer_clean for term in EDGE_CASE_TERMS):
        gaps.append("You did not mention test cases or edge cases. Add at least two to show production-level thinking.")
    if not any(term in answer_clean for term in DEPTH_TERMS):
        gaps.append("You did not discuss tradeoffs or alternatives. Add one comparison to make the answer sound more senior.")
    if not any(term in answer_clean for term in STRUCTURE_TERMS):
        gaps.append("Your answer could be more structured. Use a simple flow: define the idea, explain the approach, analyze complexity, then mention edge cases.")
    return gaps[:6]


def make_checklist(question) -> list[str]:
    checklist = [
        "Start with a one-sentence summary of the approach.",
        "Explain the main data structure or algorithm you would use.",
    ]
    for concept in question.expected_concepts[:5]:
        checklist.append(f"Mention {concept} and connect it to the solution.")
    checklist.extend([
        "State time complexity and space complexity.",
        "Give at least two edge cases or tests.",
        "End with one tradeoff, limitation, or alternative approach.",
    ])
    return checklist


def make_followups(question, missing: list[str], answer_clean: str) -> list[str]:
    followups = []
    if missing:
        followups.append(f"You did not mention {missing[0]}. How would adding that change or strengthen your answer?")
    if not any(term in answer_clean for term in COMPLEXITY_TERMS):
        followups.append("What are the time and space complexities, and why?")
    if not any(term in answer_clean for term in EDGE_CASE_TERMS):
        followups.append("What edge cases would you test before trusting this solution?")
    followups.append("What is one alternative approach, and what tradeoff would it make?")
    return followups[:3]


def make_improved_answer(question, found: list[str], missing: list[str]) -> str:
    expected = ", ".join(question.expected_concepts[:6])
    missing_text = ", ".join(missing[:4]) if missing else "no major concepts"
    return (
        f"A stronger answer should say: 'I would solve this by identifying the core pattern, then using the right structure/algorithm for it. "
        f"For this question, the key concepts are {expected}. I would explain the steps clearly, justify why the approach works, "
        f"then give time and space complexity. I would also mention edge cases and one tradeoff.' "
        f"Your current answer is mainly missing: {missing_text}."
    )


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
        clarity += 7
    if word_count >= 45:
        clarity += 6
    if word_count >= 80:
        clarity += 2
    if any(token in answer_clean for token in STRUCTURE_TERMS):
        clarity += 5

    technical_depth = 0
    if any(term in answer_clean for term in DEPTH_TERMS):
        technical_depth += 8
    if len(found) >= max(2, len(question.expected_concepts) // 2):
        technical_depth += 8
    if any(term in answer_clean for term in ["why", "because", "therefore", "so that"]):
        technical_depth += 4

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
        strengths.append("You covered these expected concepts: " + ", ".join(found[:6]) + ".")
    if clarity >= 15:
        strengths.append("Your answer has enough length and structure to be evaluated like a real interview response.")
    if complexity:
        strengths.append("You included performance analysis, which interviewers usually expect.")
    if edge_cases:
        strengths.append("You mentioned edge cases, which shows practical engineering judgment.")
    if not strengths:
        strengths.append("You attempted the question, but the answer needs more concrete technical content before it would pass an interview.")

    gaps = make_answer_gaps(answer_clean, missing, word_count)

    if missing:
        feedback = (
            "Your answer is incomplete because it misses key concepts the interviewer would likely listen for: "
            + ", ".join(missing[:6])
            + ". The biggest improvement is to explicitly name these ideas and explain how they affect the solution."
        )
    elif score >= 85:
        feedback = "Strong answer. You covered the core ideas; to make it excellent, tighten the explanation and add one clear tradeoff or edge case."
    else:
        feedback = "Good start, but it needs more interview structure: approach, why it works, complexity, edge cases, and tradeoffs."

    next_steps = []
    if missing:
        next_steps.append("Rewrite your answer and add these missing concepts: " + ", ".join(missing[:4]) + ".")
    if not complexity:
        next_steps.append("Add one sentence for time complexity and one for space complexity.")
    if not edge_cases:
        next_steps.append("Add at least two edge cases, such as empty input, duplicates, invalid input, or boundary sizes.")
    if not any(term in answer_clean for term in DEPTH_TERMS):
        next_steps.append("Add one tradeoff or alternative approach.")
    next_steps.append("Practice delivering the improved answer out loud in 60-90 seconds.")

    red_flags = []
    if word_count < 20:
        red_flags.append("The response is very short; an interviewer may think you guessed instead of reasoning through the problem.")
    if correctness < 20:
        red_flags.append("Too many expected concepts are missing, so the answer may sound surface-level.")
    if not complexity:
        red_flags.append("No Big-O analysis included.")
    if "i don't know" in answer_clean or "not sure" in answer_clean:
        red_flags.append("Uncertainty is okay, but you should follow it with a structured attempt or assumption.")

    return EvaluationResponse(
        id=str(uuid.uuid4())[:8],
        question_id=question_id,
        score=score,
        grade=grade_from_score(score),
        breakdown=breakdown,
        strengths=strengths,
        missing_concepts=missing,
        feedback=feedback,
        improved_answer=make_improved_answer(question, found, missing),
        follow_up_questions=make_followups(question, missing, answer_clean),
        next_steps=next_steps,
        answer_gaps=gaps,
        concept_feedback=make_concept_feedback(question.expected_concepts, found, missing),
        strong_answer_checklist=make_checklist(question),
        interviewer_red_flags=red_flags,
    )
