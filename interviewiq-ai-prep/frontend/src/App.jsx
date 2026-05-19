import React, { useEffect, useMemo, useState } from "react";
import { BarChart3, BrainCircuit, Clock, FileText, History, Sparkles, Target } from "lucide-react";
import { evaluateAnswer, fetchAnalytics, fetchHistory, fetchOptions, generateQuestion, generateStudyPlan, startMockInterview } from "./api/client";

const DEFAULT_OPTIONS = {
  roles: ["SWE Intern"],
  topics: ["Data Structures", "Algorithms", "System Design", "Resume Project Defense"],
  difficulties: ["Easy", "Medium", "Hard"],
  modes: ["Technical Concepts", "Timed Mock Interview", "Resume Project Defense", "Behavioral"],
};

const EMPTY_ANALYTICS = {
  total_attempts: 0,
  average_score: 0,
  strongest_topic: null,
  weakest_topic: null,
  topic_scores: {},
  recommendations: ["Complete your first practice attempt to unlock analytics."],
};

export default function App() {
  const [options, setOptions] = useState(DEFAULT_OPTIONS);
  const [candidateName, setCandidateName] = useState("Demo User");
  const [role, setRole] = useState("SWE Intern");
  const [topic, setTopic] = useState("Data Structures");
  const [difficulty, setDifficulty] = useState("Medium");
  const [mode, setMode] = useState("Technical Concepts");
  const [projectDescription, setProjectDescription] = useState("AI Interview Prep Platform built with React, FastAPI, SQLite, scoring analytics, and mock interview sessions.");
  const [question, setQuestion] = useState(null);
  const [generatedQuestionIds, setGeneratedQuestionIds] = useState([]);
  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState(null);
  const [history, setHistory] = useState([]);
  const [analytics, setAnalytics] = useState(EMPTY_ANALYTICS);
  const [studyPlan, setStudyPlan] = useState(null);
  const [mockSession, setMockSession] = useState(null);
  const [mockIndex, setMockIndex] = useState(0);
  const [timeLeft, setTimeLeft] = useState(20 * 60);
  const [timerRunning, setTimerRunning] = useState(false);
  const [loadingQuestion, setLoadingQuestion] = useState(false);
  const [loadingEvaluation, setLoadingEvaluation] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => { loadInitialData(); }, []);

  useEffect(() => {
    if (!timerRunning) return;
    const id = setInterval(() => setTimeLeft((t) => Math.max(0, t - 1)), 1000);
    return () => clearInterval(id);
  }, [timerRunning]);

  const formattedTime = useMemo(() => {
    const min = Math.floor(timeLeft / 60).toString().padStart(2, "0");
    const sec = (timeLeft % 60).toString().padStart(2, "0");
    return `${min}:${sec}`;
  }, [timeLeft]);

  async function loadInitialData() {
    try {
      setOptions(await fetchOptions());
      setHistory(await fetchHistory());
      setAnalytics(await fetchAnalytics());
    } catch (err) { setError(err.message); }
  }

  async function refreshInsights() {
    setHistory(await fetchHistory());
    setAnalytics(await fetchAnalytics());
  }

  async function onGenerateQuestion() {
    setLoadingQuestion(true); setError(""); setEvaluation(null); setAnswer(""); setMockSession(null); setTimerRunning(false);
    try {
      const nextQuestion = await generateQuestion({ role, topic, difficulty, mode, project_description: projectDescription, exclude_ids: generatedQuestionIds });
      setQuestion(nextQuestion);
      setGeneratedQuestionIds((prev) => prev.includes(nextQuestion.id) ? [nextQuestion.id] : [...prev, nextQuestion.id]);
    } catch (err) { setError(err.message); }
    finally { setLoadingQuestion(false); }
  }

  async function onEvaluate() {
    if (!question) return;
    setLoadingEvaluation(true); setError("");
    try {
      setEvaluation(await evaluateAnswer({ question_id: question.id, answer, candidate_name: candidateName }));
      await refreshInsights();
    } catch (err) { setError(err.message); }
    finally { setLoadingEvaluation(false); }
  }

  async function onStudyPlan() {
    setError("");
    try { setStudyPlan(await generateStudyPlan({ days: 7 })); }
    catch (err) { setError(err.message); }
  }

  async function onStartMock() {
    setError(""); setEvaluation(null); setAnswer("");
    try {
      const session = await startMockInterview({ role, difficulty, question_count: 5 });
      setMockSession(session); setMockIndex(0); setQuestion(session.questions[0]);
      setTimeLeft(session.time_limit_minutes * 60); setTimerRunning(true);
    } catch (err) { setError(err.message); }
  }

  function nextMockQuestion() {
    if (!mockSession) return;
    const next = Math.min(mockIndex + 1, mockSession.questions.length - 1);
    setMockIndex(next); setQuestion(mockSession.questions[next]); setAnswer(""); setEvaluation(null);
  }

  function loadInterviewDemo() {
    setCandidateName("Bhavin Demo");
    setRole("SWE Intern");
    setTopic("Data Structures");
    setDifficulty("Medium");
    setMode("Technical Concepts");
    setGeneratedQuestionIds([]);
    setProjectDescription("InterviewIQ, a React and FastAPI platform that generates technical interview questions, evaluates answers with a rubric, tracks weaknesses in SQLite, and creates study plans.");
  }

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow"><Sparkles size={16} /> Enhanced Flagship SWE Portfolio Project</p>
          <h1><BrainCircuit size={42} /> InterviewIQ</h1>
          <p>Practice technical interviews, run timed mock sessions, defend resume projects, receive rubric-based feedback, and track improvement.</p>
        </div>
        <button className="secondary" onClick={loadInterviewDemo}>Load Interview Demo</button>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <main className="layout">
        <section className="card setup-card">
          <h2><Target size={22} /> Setup</h2>
          <label>Candidate name<input value={candidateName} onChange={(e) => setCandidateName(e.target.value)} /></label>
          <label>Role<select value={role} onChange={(e) => setRole(e.target.value)}>{options.roles.map((r) => <option key={r}>{r}</option>)}</select></label>
          <label>Mode<select value={mode} onChange={(e) => { setMode(e.target.value); if (e.target.value === "Resume Project Defense") setTopic("Resume Project Defense"); }}>{options.modes.map((m) => <option key={m}>{m}</option>)}</select></label>
          <label>Topic<select value={topic} onChange={(e) => setTopic(e.target.value)}>{options.topics.map((t) => <option key={t}>{t}</option>)}</select></label>
          <label>Difficulty<select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>{options.difficulties.map((d) => <option key={d}>{d}</option>)}</select></label>
          {(mode === "Resume Project Defense" || topic === "Resume Project Defense") && <label>Project description<textarea value={projectDescription} onChange={(e) => setProjectDescription(e.target.value)} rows={5} /></label>}
          <div className="button-grid">
            <button className="primary" onClick={onGenerateQuestion} disabled={loadingQuestion}>{loadingQuestion ? "Generating..." : "Generate Question"}</button>
            <button className="secondary-outline" onClick={onStartMock}><Clock size={16}/> Start Mock</button>
            <button className="secondary-outline" onClick={onStudyPlan}><FileText size={16}/> Study Plan</button>
          </div>
        </section>

        <section className="card analytics-card">
          <h2><BarChart3 size={22} /> Progress Dashboard</h2>
          <div className="metrics">
            <div><strong>{analytics.total_attempts}</strong><span>Attempts</span></div>
            <div><strong>{analytics.average_score}</strong><span>Avg score</span></div>
            <div><strong>{analytics.weakest_topic || "—"}</strong><span>Weakest</span></div>
          </div>
          <div className="topic-bars">
            {Object.entries(analytics.topic_scores || {}).map(([name, score]) => <div key={name}><span>{name}</span><div className="bar"><b style={{ width: `${score}%` }} /></div><em>{score}</em></div>)}
          </div>
          <ul className="compact-list">{analytics.recommendations.map((r) => <li key={r}>{r}</li>)}</ul>
        </section>

        <section className="card question-card">
          <div className="question-head">
            <h2>Current Question</h2>
            {mockSession && <div className="timer"><Clock size={16}/>{formattedTime} · Q{mockIndex + 1}/{mockSession.questions.length}</div>}
          </div>
          {!question && <p className="muted">Click Generate Question or Start Mock to begin.</p>}
          {question && <>
            <div className="pill-row"><span>{question.role}</span><span>{question.topic}</span><span>{question.difficulty}</span></div>
            <h3>{question.question}</h3>
            <details><summary>Hints</summary><ul>{question.hints.map((h) => <li key={h}>{h}</li>)}</ul></details>
            <label>Your answer<textarea value={answer} onChange={(e) => setAnswer(e.target.value)} rows={8} placeholder="Type your interview answer here. Include approach, complexity, tradeoffs, and edge cases." /></label>
            <div className="button-grid">
              <button className="primary" onClick={onEvaluate} disabled={loadingEvaluation || !answer.trim()}>{loadingEvaluation ? "Evaluating..." : "Evaluate Answer"}</button>
              {mockSession && <button className="secondary-outline" onClick={nextMockQuestion} disabled={mockIndex >= mockSession.questions.length - 1}>Next Mock Question</button>}
            </div>
          </>}
        </section>

        <section className="card evaluation-card">
          <h2>Rubric Feedback</h2>
          {!evaluation && <p className="muted">Submit an answer to see rubric scoring.</p>}
          {evaluation && <>
            <div className="score"><strong>{evaluation.score}</strong><span>{evaluation.grade}</span></div>
            <div className="rubric">
              {Object.entries(evaluation.breakdown).map(([k, v]) => <div key={k}><span>{k.replace("_", " ")}</span><b>{v}</b></div>)}
            </div>
            <h3>Specific Feedback</h3><p>{evaluation.feedback}</p>
            {evaluation.answer_gaps?.length > 0 && <>
              <h3>What You Are Missing</h3>
              <ul className="gap-list">{evaluation.answer_gaps.map((gap) => <li key={gap}>{gap}</li>)}</ul>
            </>}
            {evaluation.concept_feedback?.length > 0 && <>
              <h3>Concept-by-Concept Breakdown</h3>
              <div className="concept-grid">
                {evaluation.concept_feedback.map((item) => <article className={item.status === "covered" ? "concept covered" : "concept missing"} key={item.concept}>
                  <div><strong>{item.concept}</strong><span>{item.status}</span></div>
                  <p>{item.why_it_matters}</p>
                  {item.status !== "covered" && <small>{item.how_to_add_it}</small>}
                </article>)}
              </div>
            </>}
            {evaluation.interviewer_red_flags?.length > 0 && <>
              <h3>Interviewer Red Flags</h3>
              <ul className="red-flags">{evaluation.interviewer_red_flags.map((flag) => <li key={flag}>{flag}</li>)}</ul>
            </>}
            <h3>Strengths</h3><ul>{evaluation.strengths.map((s) => <li key={s}>{s}</li>)}</ul>
            <h3>Follow-up Questions</h3><ul>{evaluation.follow_up_questions.map((q) => <li key={q}>{q}</li>)}</ul>
            <h3>Strong Answer Checklist</h3><ul>{evaluation.strong_answer_checklist?.map((s) => <li key={s}>{s}</li>)}</ul>
            <h3>Improved Answer Template</h3><p className="improved">{evaluation.improved_answer}</p>
            <h3>Next Steps</h3><ul>{evaluation.next_steps.map((s) => <li key={s}>{s}</li>)}</ul>
          </>}
        </section>

        {studyPlan && <section className="card study-card">
          <h2><FileText size={22}/> 7-Day Study Plan</h2>
          <p>{studyPlan.summary}</p>
          <div className="study-grid">{studyPlan.days.map((day) => <article key={day.day}><h3>Day {day.day}: {day.focus}</h3><ul>{day.tasks.map((t) => <li key={t}>{t}</li>)}</ul></article>)}</div>
        </section>}

        <section className="card history-card">
          <h2><History size={22}/> Saved Answer History</h2>
          {history.length === 0 && <p className="muted">No attempts yet.</p>}
          {history.map((item) => <details className="history-item" key={item.id}><summary><strong>{item.score}</strong> · {item.topic} · {item.grade}<span>{item.created_at}</span></summary><p><b>Question:</b> {item.question}</p><p><b>Your answer:</b> {item.answer}</p><p><b>Feedback:</b> {item.feedback}</p></details>)}
        </section>
      </main>
    </div>
  );
}
