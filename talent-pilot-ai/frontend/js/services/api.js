import { API_BASE } from "../config.js";

async function parseJson(response) {
  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error("Unexpected response from server.");
  }
  if (!response.ok || payload.success === false) {
    const message = payload?.error?.message || `Request failed (${response.status})`;
    const error = new Error(message);
    error.code = payload?.error?.code;
    error.status = response.status;
    throw error;
  }
  return payload;
}

export async function analyzeResume(resumeFile, jobDescription) {
  const formData = new FormData();
  formData.append("resume", resumeFile);
  formData.append("job_description", jobDescription);
  const response = await fetch(`${API_BASE}/api/v1/analyze`, {
    method: "POST",
    body: formData,
    credentials: "include",
  });
  const payload = await parseJson(response);
  return { analysis: payload.analysis, savedId: payload.saved_id ?? null };
}

export async function register(email, password) {
  const response = await fetch(`${API_BASE}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ email, password }),
  });
  return (await parseJson(response)).user;
}

export async function login(email, password) {
  const response = await fetch(`${API_BASE}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ email, password }),
  });
  return (await parseJson(response)).user;
}

export async function logout() {
  await fetch(`${API_BASE}/api/v1/auth/logout`, { method: "POST", credentials: "include" });
}

export async function getMe() {
  const response = await fetch(`${API_BASE}/api/v1/auth/me`, { credentials: "include" });
  if (response.status === 401) return null;
  return (await parseJson(response)).user;
}

export async function fetchSavedHistory() {
  const response = await fetch(`${API_BASE}/api/v1/history`, { credentials: "include" });
  if (response.status === 401) return [];
  return (await parseJson(response)).items;
}

export async function fetchSampleJobDescription() {
  const response = await fetch(`${API_BASE}/api/v1/samples/job-description`);
  return (await parseJson(response)).job_description;
}

export async function fetchSampleResumeFile() {
  const response = await fetch(`${API_BASE}/api/v1/samples/resume`);
  if (!response.ok) throw new Error("Could not load demo resume.");
  const blob = await response.blob();
  return new File([blob], "demo-resume.pdf", { type: "application/pdf" });
}
