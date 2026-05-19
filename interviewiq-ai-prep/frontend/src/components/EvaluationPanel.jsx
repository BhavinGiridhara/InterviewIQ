import { CheckCircle2, Target } from "lucide-react";

export default function EvaluationPanel({ evaluation }) {
  if (!evaluation) return <section className="card empty"><h2><Target size={22} /> Feedback</h2><p>Your score and feedback will appear here after evaluation.</p></section>;
  return (
    <section className="card feedback">
      <div className="score-header"><div><p className="eyebrow">Evaluation</p><h2>{evaluation.grade}</h2></div><div className="score">{evaluation.score}</div></div>
      <h3><CheckCircle2 size={18} /> Strengths</h3><ul>{evaluation.strengths.map((item) => <li key={item}>{item}</li>)}</ul>
      <h3>Missing Concepts</h3>{evaluation.missing_concepts.length ? <div className="tag-row">{evaluation.missing_concepts.map((item) => <span key={item}>{item}</span>)}</div> : <p className="success">No major expected concepts missing.</p>}
      <h3>Feedback</h3><p>{evaluation.feedback}</p>
      <h3>Improved Answer Template</h3><p className="improved">{evaluation.improved_answer}</p>
      <h3>Next Steps</h3><ul>{evaluation.next_steps.map((item) => <li key={item}>{item}</li>)}</ul>
    </section>
  );
}
