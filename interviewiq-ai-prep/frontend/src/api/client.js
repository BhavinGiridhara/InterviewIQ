const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || `Request failed: ${response.status}`);
  }
  return response.json();
}

export function fetchOptions() { return request("/api/options"); }
export function generateQuestion(payload) { return request("/api/question", { method: "POST", body: JSON.stringify(payload) }); }
export function evaluateAnswer(payload) { return request("/api/evaluate", { method: "POST", body: JSON.stringify(payload) }); }
export function fetchHistory(name = "Demo User") { return request(`/api/history?candidate_name=${encodeURIComponent(name)}`); }
export function fetchAnalytics(name = "Demo User") { return request(`/api/analytics?candidate_name=${encodeURIComponent(name)}`); }
export function generateStudyPlan(payload) { return request("/api/study-plan", { method: "POST", body: JSON.stringify(payload) }); }
export function startMockInterview(payload) { return request("/api/mock-interview", { method: "POST", body: JSON.stringify(payload) }); }

export function previewAnswer(payload) { return request("/api/evaluate-preview", { method: "POST", body: JSON.stringify(payload) }); }
export function removeHistory(name, id) { return request(`/api/history${id ? "/" + encodeURIComponent(id) : ""}?candidate_name=${encodeURIComponent(name)}`, { method: "DELETE" }); }
export function restoreHistory(name, batch) { return request(`/api/history/restore/${encodeURIComponent(batch)}?candidate_name=${encodeURIComponent(name)}`, { method: "POST" }); }
