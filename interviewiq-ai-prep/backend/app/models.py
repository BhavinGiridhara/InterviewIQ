from typing import List, Optional
from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    role: str = "SWE Intern"
    topic: str = "Data Structures"
    difficulty: str = "Medium"
    mode: str = "Technical Concepts"
    exclude_ids: List[str] = []
    project_description: Optional[str] = None

class InterviewQuestion(BaseModel):
    id: str
    role: str
    topic: str
    difficulty: str
    question: str
    expected_concepts: List[str]
    hints: List[str]

class EvaluationRequest(BaseModel):
    question_id: str
    answer: str = Field(min_length=1)
    candidate_name: Optional[str] = "Demo User"

class ScoreBreakdown(BaseModel):
    correctness: int
    clarity: int
    technical_depth: int
    edge_cases: int
    complexity: int

class ConceptFeedback(BaseModel):
    concept: str
    status: str
    why_it_matters: str
    how_to_add_it: str

class EvaluationResponse(BaseModel):
    id: str
    question_id: str
    score: int
    grade: str
    breakdown: ScoreBreakdown
    strengths: List[str]
    missing_concepts: List[str]
    feedback: str
    improved_answer: str
    follow_up_questions: List[str]
    next_steps: List[str]
    answer_gaps: List[str] = []
    concept_feedback: List[ConceptFeedback] = []
    strong_answer_checklist: List[str] = []
    interviewer_red_flags: List[str] = []

class AnalyticsResponse(BaseModel):
    total_attempts: int
    average_score: float
    strongest_topic: Optional[str]
    weakest_topic: Optional[str]
    topic_scores: dict
    recommendations: List[str]

class StudyPlanRequest(BaseModel):
    days: int = Field(default=7, ge=3, le=14)

class StudyDay(BaseModel):
    day: int
    focus: str
    tasks: List[str]

class StudyPlanResponse(BaseModel):
    summary: str
    days: List[StudyDay]

class MockInterviewRequest(BaseModel):
    role: str = "SWE Intern"
    difficulty: str = "Medium"
    question_count: int = Field(default=5, ge=3, le=8)

class MockInterviewResponse(BaseModel):
    session_id: str
    time_limit_minutes: int
    questions: List[InterviewQuestion]
