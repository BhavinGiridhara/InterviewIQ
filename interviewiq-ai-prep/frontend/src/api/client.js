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
export function fetchHistory() { return request("/api/history"); }
export function fetchAnalytics() { return request("/api/analytics"); }
export function generateStudyPlan(payload) { return request("/api/study-plan", { method: "POST", body: JSON.stringify(payload) }); }
export function startMockInterview(payload) { return request("/api/mock-interview", { method: "POST", body: JSON.stringify(payload) }); }
