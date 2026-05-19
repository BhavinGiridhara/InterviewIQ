import { MessageSquareText } from "lucide-react";

export default function QuestionCard({ question, answer, setAnswer, onEvaluate, loading }) {
  if (!question) return <section className="card empty"><h2><MessageSquareText size={22} /> Interview Question</h2><p>Choose your setup and generate a question to begin.</p></section>;
  return (
    <section className="card question-card">
      <h2><MessageSquareText size={22} /> Interview Question</h2>
      <div className="pill-row"><span>{question.role}</span><span>{question.topic}</span><span>{question.difficulty}</span></div>
      <h3>{question.question}</h3>
      <details><summary>Need hints?</summary><ul>{question.hints.map((hint) => <li key={hint}>{hint}</li>)}</ul></details>
      <label>Your answer<textarea value={answer} onChange={(event) => setAnswer(event.target.value)} placeholder="Type your answer like you would explain it to an interviewer..." /></label>
      <button className="primary" onClick={onEvaluate} disabled={loading || !answer.trim()}>{loading ? "Evaluating..." : "Evaluate Answer"}</button>
    </section>
  );
}
