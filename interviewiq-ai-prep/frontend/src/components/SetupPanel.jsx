import { SlidersHorizontal } from "lucide-react";

export default function SetupPanel({ options, role, setRole, topic, setTopic, difficulty, setDifficulty, candidateName, setCandidateName, onGenerate, loading }) {
  return (
    <section className="card">
      <h2><SlidersHorizontal size={22} /> Practice Setup</h2>
      <label>Candidate name<input value={candidateName} onChange={(event) => setCandidateName(event.target.value)} /></label>
      <label>Role<select value={role} onChange={(event) => setRole(event.target.value)}>{options.roles.map((item) => <option key={item}>{item}</option>)}</select></label>
      <label>Topic<select value={topic} onChange={(event) => setTopic(event.target.value)}>{options.topics.map((item) => <option key={item}>{item}</option>)}</select></label>
      <label>Difficulty<select value={difficulty} onChange={(event) => setDifficulty(event.target.value)}>{options.difficulties.map((item) => <option key={item}>{item}</option>)}</select></label>
      <button className="primary" onClick={onGenerate} disabled={loading}>{loading ? "Generating..." : "Generate Question"}</button>
    </section>
  );
}
