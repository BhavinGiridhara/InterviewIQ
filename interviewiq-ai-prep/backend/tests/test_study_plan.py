import unittest
from app.study_plan import build_study_plan


def attempt(question_id, topic, score, **extra):
    return dict(question_id=question_id, topic=topic, score=score,
                question=f"Explain {question_id}", **extra)


class StudyPlanTests(unittest.TestCase):
    def test_empty_history_has_no_invented_plan(self):
        self.assertEqual(build_study_plan([], 7)["days"], [])

    def test_weak_topics_and_actual_feedback_drive_tasks(self):
        history = [attempt("hash", "Data Structures", 25, missing_concepts="collision, hashing", feedback="Explain collisions."), attempt("api", "System Design", 95)]
        plan = build_study_plan(history, 7)
        self.assertEqual(len(plan["days"]), 7)
        self.assertGreater(sum(d["focus"] == "Data Structures" for d in plan["days"]), 3)
        text = " ".join(plan["days"][0]["tasks"])
        self.assertIn("Explain hash", text)
        self.assertIn("collision, hashing", text)
        self.assertIn("Explain collisions.", text)
        self.assertEqual(plan, build_study_plan(history, 7))

    def test_improvement_replaces_old_weakness(self):
        old = [attempt("hash", "Data Structures", 10, missing_concepts="collision"), attempt("api", "System Design", 50)]
        self.assertEqual(build_study_plan(old, 3)["days"][0]["focus"], "Data Structures")
        new = [attempt("hash", "Data Structures", 100)] + old
        plan = build_study_plan(new, 3)
        self.assertEqual(plan["days"][0]["focus"], "System Design")
        self.assertNotIn("collision", str(plan))

    def test_rubric_comparison_uses_percentages_and_skips_nulls(self):
        history = [attempt("hash", "Data Structures", 65, correctness=20, clarity=None, complexity=15, edge_cases=10, technical_depth=20)]
        text = " ".join(build_study_plan(history, 7)["days"][0]["tasks"])
        self.assertIn("Explain the core concepts accurately", text)
        self.assertNotIn("Add two concrete edge cases", text)
        self.assertNotIn("State and justify", text)

    def test_single_topic_supports_all_plan_lengths(self):
        for days in (3, 7, 14):
            plan = build_study_plan([attempt("oop", "OOP", 80)], days)
            self.assertEqual(len(plan["days"]), days)
            self.assertEqual({d["focus"] for d in plan["days"]}, {"OOP"})


if __name__ == "__main__":
    unittest.main()
