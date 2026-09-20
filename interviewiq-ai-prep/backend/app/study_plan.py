"""Build a deterministic study plan from the candidate's saved answers."""
from collections import Counter, defaultdict


RUBRICS = {
    "correctness": (40, "Explain the core concepts accurately and check them against your notes."),
    "clarity": (20, "Rewrite your answer as a clear sequence: first, then, finally."),
    "technical_depth": (20, "Explain why your approach works and compare one alternative or tradeoff."),
    "edge_cases": (10, "Add two concrete edge cases and explain how you would handle them."),
    "complexity": (15, "State and justify the time and space complexity of your approach."),
}


def build_study_plan(attempts: list[dict], days: int) -> dict:
    if not attempts:
        return {"summary": "No saved answers for this candidate yet. Answer and evaluate a few questions, then generate a study plan.", "days": []}

    # Latest performance on each question avoids repeatedly penalizing a fixed mistake.
    latest = {}
    for attempt in attempts:  # Repository supplies newest first.
        key = attempt.get("question_id") or (attempt["topic"], attempt["question"])
        latest.setdefault(key, attempt)
    buckets = defaultdict(list)
    for attempt in latest.values():
        buckets[attempt["topic"]].append(attempt)
    averages = {topic: sum(a["score"] for a in rows) / len(rows) for topic, rows in buckets.items()}
    topics = sorted(buckets, key=lambda topic: (averages[topic], topic))
    # Every practiced topic is eligible; larger deficits receive more review days.
    weights = {topic: max(10, 100 - averages[topic]) for topic in topics}
    assigned = Counter()
    plan = []
    for day in range(1, days + 1):
        topic = max(topics, key=lambda t: weights[t] / (assigned[t] + 1))
        rows = sorted(buckets[topic], key=lambda a: (a["score"], a["question"]))
        visit = assigned[topic]
        target = rows[visit % len(rows)]
        missing = Counter(concept.strip() for row in rows for concept in (row.get("missing_concepts") or "").split(",") if concept.strip())
        rubric_scores = {}
        for name, (maximum, _) in RUBRICS.items():
            values = [row[name] / maximum for row in rows if row.get(name) is not None]
            if values:
                rubric_scores[name] = sum(values) / len(values)
        weak_rubrics = sorted(rubric_scores, key=rubric_scores.get)[:2]
        tasks = [f"{'Revisit' if visit else 'Review'} {topic}: your latest-answer average is {averages[topic]:.1f}/100."]
        if missing:
            tasks.append("Review missed concepts: " + ", ".join(c for c, _ in missing.most_common(4)) + ". Explain each in your own words.")
        tasks.append(f'Retry this saved question without looking at your old answer (previous score {target["score"]}/100): {target["question"]}')
        if target.get("feedback"):
            tasks.append("Use your saved feedback: " + target["feedback"])
        tasks.extend(RUBRICS[name][1] for name in weak_rubrics if rubric_scores[name] < 1)
        if visit:
            tasks.append("Give your revised answer out loud in 90 seconds, then explain a different example.")
        tasks.append("Evaluate your revised answer and compare its score and missed concepts with the saved attempt. Regenerate the plan after practicing.")
        plan.append({"day": day, "focus": topic, "tasks": tasks})
        assigned[topic] += 1
    return {"summary": f"Based on {len(attempts)} saved attempts and the latest answers to {len(latest)} distinct questions. Prioritize {topics[0]} ({averages[topics[0]]:.1f}/100); weaker topics receive more practice. Rubric priorities use each category's maximum score.", "days": plan}
