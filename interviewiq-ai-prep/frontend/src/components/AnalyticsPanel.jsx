import { BarChart3 } from "lucide-react";

export default function AnalyticsPanel({ analytics, history }) {
  return (
    <section className="card analytics">
      <h2><BarChart3 size={22} /> Progress Analytics</h2>
      <div className="metric-grid"><div><strong>{analytics.total_attempts}</strong><span>Attempts</span></div><div><strong>{analytics.average_score}</strong><span>Avg Score</span></div><div><strong>{analytics.weakest_topic || "—"}</strong><span>Weakest Topic</span></div></div>
      <h3>Recommendations</h3><ul>{analytics.recommendations.map((item) => <li key={item}>{item}</li>)}</ul>
      <h3>Recent Attempts</h3>{history.length === 0 && <p className="muted">No attempts yet.</p>}
      {history.map((item) => <div className="history-item" key={item.id}><div><strong>{item.topic}</strong><p>{item.question}</p></div><span>{item.score} · {item.grade}</span></div>)}
    </section>
  );
}
