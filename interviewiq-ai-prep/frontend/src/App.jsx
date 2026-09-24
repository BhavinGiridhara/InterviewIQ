import React, { useEffect, useMemo, useState } from "react";
import { BarChart3, BrainCircuit, Clock, FileText, History, Sparkles, Target } from "lucide-react";
import { evaluateAnswer, fetchAnalytics, fetchHistory, fetchOptions, generateQuestion, generateStudyPlan, startMockInterview } from "./api/client";

const DEFAULT_OPTIONS = {
  roles: ["SWE Intern"],
  topics: ["Data Structures", "Algorithms", "System Design", "Resume Project Defense"],
  difficulties: ["Easy", "Medium", "Hard"],
  modes: ["Technical Concepts", "Timed Mock Interview", "Resume Project Defense", "Behavioral"],
};

const RUBRIC_MAX = { correctness: 40, clarity: 20, technical_depth: 20, edge_cases: 10, complexity: 15 };

const EMPTY_ANALYTICS = {
  total_attempts: 0,
  average_score: 0,
  strongest_topic: null,
  weakest_topic: null,
  topic_scores: {},
  recommendations: ["Complete your first practice attempt to unlock analytics."],
};

export default function App() {
  const [activeTab, setActiveTab] = useState("practice");
  const [sampleLoaded, setSampleLoaded] = useState(false);
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

  useEffect(() => { setStudyPlan(null); }, [candidateName]);

  async function refreshInsights() {
    setStudyPlan(null);
    setHistory(await fetchHistory());
    setAnalytics(await fetchAnalytics());
  }

  async function onGenerateQuestion() {
    setSampleLoaded(false); setActiveTab("practice");
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
    setActiveTab("progress"); setError("");
    try { setStudyPlan(await generateStudyPlan({ days: 7, candidate_name: candidateName || "Demo User" })); }
    catch (err) { setError(err.message); }
  }

  async function onStartMock() {
    setSampleLoaded(false); setActiveTab("practice");
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

  function loadSample() {
    setActiveTab("practice"); setError(""); setEvaluation(null); setMockSession(null); setTimerRunning(false);
    setRole("SWE Intern"); setTopic("Data Structures"); setDifficulty("Easy"); setMode("Technical Concepts");
    setQuestion({ id: "ds-array-vs-linkedlist-easy", role: "SWE Intern", topic: "Data Structures", difficulty: "Easy",
      question: "What is the difference between an array and a linked list? When would you use each?",
      hints: ["Compare random access.", "Mention insertion/deletion tradeoffs.", "Use Big-O."] });
    setAnswer("First, an array stores elements in contiguous memory and supports O(1) indexing. A linked list stores nodes connected by pointers, so finding an element by index takes O(n). To insert or delete in the middle of an array, elements usually need to shift. With a linked list, updating links is O(1) once the required node and predecessor are known, but finding that position is O(n). For example, I would choose an array for frequent random access because it has good memory locality. The tradeoff is that a linked list supports flexible node insertion but uses extra memory for pointers. Finally, I would test an empty collection, a single element, and operations at the head and tail.");
    setSampleLoaded(true);
  }

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow"><Sparkles size={16} /> Technical Interview Practice</p>
          <h1><BrainCircuit size={32} /> InterviewIQ</h1>
          <p>Practice. Get feedback. Track your progress.</p>
        </div>
      </header>

      {error && <div role="alert" className="error-banner">{error}</div>}

      <nav className="view-nav" aria-label="Workspace views">
        {[["practice", "Practice", Target], ["progress", "Progress", BarChart3], ["history", "History", History]].map(([id, label, Icon]) =>
          <button key={id} aria-pressed={activeTab === id} onClick={() => setActiveTab(id)}><Icon size={18}/>{label}</button>)}
      </nav>
      <main className={`layout view-${activeTab}`}>

        <section className="card setup-card" hidden={activeTab !== "practice"}>
          <h2><Target size={20} /> Your session</h2>
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

        <section className="card analytics-card" hidden={activeTab !== "progress"}>
          <div className="section-heading"><div><p className="section-kicker">Keep improving</p><h2><BarChart3 size={22} /> Progress Dashboard</h2></div><button className="secondary-outline" onClick={onStudyPlan}><FileText size={16}/> Create study plan</button></div><p className="muted">Scores across all saved practice attempts.</p>
          <div className="metrics">
            <div><strong>{analytics.total_attempts}</strong><span>Attempts</span></div>
            <div><strong>{analytics.average_score}</strong><span>Avg score</span></div>
            <div><strong>{analytics.weakest_topic || "—"}</strong><span>Topic to focus on</span></div>
          </div>
          <div className="topic-bars">
            {Object.entries(analytics.topic_scores || {}).map(([name, score]) => <div key={name}><span>{name}</span><div className="bar"><b style={{ width: `${score}%` }} /></div><em>{score}</em></div>)}
          </div>
          <ul className="compact-list">{analytics.recommendations.map((r) => <li key={r}>{r}</li>)}</ul>
        </section>

        <section className="card question-card" hidden={activeTab !== "practice"}>
          <div className="question-head">
            <div><p className="section-kicker">01 / Practice</p><h2>{question ? "Your next challenge" : "Make your next interview feel familiar."}</h2></div>
            {mockSession && <div className="timer"><Clock size={16}/>{formattedTime} · Q{mockIndex + 1}/{mockSession.questions.length}</div>}
          </div>
          {!question && <div className="empty-state"><Target size={40}/><h3>One question. A clearer next step.</h3><p>Choose your topic and difficulty, then generate a question. Explain your approach in your own words and get structured feedback.</p><div className="workflow"><span>1. Choose a question</span><span>2. Explain your approach</span><span>3. Review feedback</span></div></div>}
          {!mockSession && <div className="sample-row"><button className="text-button" onClick={loadSample} disabled={Boolean(answer.trim()) || loadingQuestion || loadingEvaluation}>Try a sample answer</button><span>{answer.trim() ? "Clear your answer to load an example." : "Loads an example question and answer."}</span></div>}
          {question && <>
            <div className="pill-row"><span>{question.role}</span><span>{question.topic}</span><span>{question.difficulty}</span></div>
            <h3>{question.question}</h3>
            <details><summary>Hints</summary><ul>{question.hints.map((h) => <li key={h}>{h}</li>)}</ul></details>
            {sampleLoaded && <p className="sample-notice">Example answer loaded. Evaluating it will save an attempt and include it in your progress.</p>}
            <label>Your answer<textarea value={answer} onChange={(e) => setAnswer(e.target.value)} rows={8} placeholder="Type your interview answer here. Include approach, complexity, tradeoffs, and edge cases." /></label>
            <div className="answer-actions"><span className="muted">{answer.trim() ? answer.trim().split(/\s+/).length : 0} words</span>
              <button className="primary" onClick={onEvaluate} disabled={loadingEvaluation || !answer.trim()}>{loadingEvaluation ? "Evaluating..." : "Evaluate Answer"}</button>
              {mockSession && <button className="secondary-outline" onClick={nextMockQuestion} disabled={mockIndex >= mockSession.questions.length - 1}>Next Mock Question</button>}
            </div>
          </>}
        </section>

        <section className="card evaluation-card" hidden={activeTab !== "practice" || !evaluation} aria-live="polite">
          <p className="section-kicker">02 / Reflect</p><h2>Turn feedback into progress</h2>
          {!evaluation && <p className="muted">Submit an answer to see rubric scoring.</p>}
          {evaluation && <>
            <div className="score"><strong>{evaluation.score}<small> / 100</small></strong><span>{evaluation.grade}</span></div>
            <div className="rubric">
              {Object.entries(evaluation.breakdown).map(([k, v]) => <div key={k}><span>{k.replaceAll("_", " ")}</span><b>{v} <small>/ {RUBRIC_MAX[k]}</small></b><progress aria-label={k.replaceAll("_", " ")} value={v} max={RUBRIC_MAX[k]} /></div>)}
            </div>
            <h3>Feedback</h3><p>{evaluation.feedback}</p>
            <h3>Strengths</h3><ul>{evaluation.strengths.map((s) => <li key={s}>{s}</li>)}</ul>
            <h3>Follow-up Questions</h3><ul>{evaluation.follow_up_questions.map((q) => <li key={q}>{q}</li>)}</ul>
            <h3>Improved Answer Template</h3><p className="improved">{evaluation.improved_answer}</p>
            <h3>Areas to improve</h3><ul>{evaluation.next_steps.map((s) => <li key={s}>{s}</li>)}</ul>
          </>}
        </section>

        {studyPlan && <section className="card study-card" hidden={activeTab !== "progress"}>
          <h2><FileText size={22}/> 7-Day Study Plan</h2>
          <p>{studyPlan.summary}</p>
          <div className="study-grid">{studyPlan.days.map((day) => <article key={day.day}><h3>Day {day.day}: {day.focus}</h3><ul>{day.tasks.map((t) => <li key={t}>{t}</li>)}</ul></article>)}</div>
        </section>}

        <section className="card history-card" hidden={activeTab !== "history"}>
          <h2><History size={22}/> Saved Answer History</h2>
          {history.length === 0 && <p className="muted">Your practice story starts here. Evaluate an answer in Practice to save your first attempt.</p>}
          {history.map((item) => <details className="history-item" key={item.id}><summary><strong>{item.score}<small> / 100</small></strong><span className="history-topic">{item.topic} · {item.grade}</span><time>{item.created_at}</time></summary><p><b>Question:</b> {item.question}</p><p><b>Your answer:</b> {item.answer}</p><p><b>Feedback:</b> {item.feedback}</p></details>)}
        </section>
      </main>
    </div>
  );
}

