import {
  analyzeResume,
  fetchSampleJobDescription,
  fetchSampleResumeFile,
  fetchSavedHistory,
  getMe,
  login,
  logout,
  register,
} from "./api.js";
import { downloadMarkdown, exportPdfPrint } from "./export.js";
import {
  addSessionHistoryItem,
  getSessionHistory,
  renderHistoryList,
} from "./history.js";
import { getCurrentAnalysis, hideResults, renderResults } from "./results.js";

const form = document.getElementById("analyze-form");
const submitBtn = document.getElementById("submit-btn");
const statusEl = document.getElementById("status");
const jdInput = document.getElementById("job_description");
const jdCount = document.getElementById("jd-count");
const resumeInput = document.getElementById("resume");
const resumeName = document.getElementById("resume-name");

let currentUser = null;
let authMode = "login";
let sampleFile = null;

function setStatus(kind, message) {
  statusEl.classList.remove("hidden", "loading", "error");
  if (!message) {
    statusEl.classList.add("hidden");
    statusEl.textContent = "";
    return;
  }
  statusEl.classList.add(kind);
  statusEl.textContent = message;
}

function refreshSessionHistory() {
  renderHistoryList(document.getElementById("session-history"), getSessionHistory(), (item) => {
    renderResults(item.analysis);
    setStatus("", "");
  });
}

async function refreshSavedHistory() {
  const listEl = document.getElementById("saved-history");
  const hint = document.getElementById("saved-history-hint");
  if (!currentUser) {
    hint.textContent = "Sign in to save analyses.";
    listEl.innerHTML = "";
    return;
  }
  hint.textContent = `Signed in as ${currentUser.email}`;
  try {
    const items = await fetchSavedHistory();
    renderHistoryList(listEl, items, (item) => {
      renderResults(item.analysis);
      setStatus("", "");
    });
  } catch (err) {
    hint.textContent = err.message || "Could not load saved history.";
  }
}

function updateAuthBar() {
  const status = document.getElementById("auth-status");
  const openBtn = document.getElementById("auth-open-btn");
  const logoutBtn = document.getElementById("logout-btn");
  if (currentUser) {
    status.textContent = currentUser.email;
    openBtn.classList.add("hidden");
    logoutBtn.classList.remove("hidden");
  } else {
    status.textContent = "Not signed in";
    openBtn.classList.remove("hidden");
    logoutBtn.classList.add("hidden");
  }
}

function setAuthMode(mode) {
  authMode = mode;
  const loginTab = document.getElementById("tab-login");
  const registerTab = document.getElementById("tab-register");
  if (mode === "login") {
    loginTab.className = "px-3 py-1 bg-sea text-white";
    registerTab.className = "px-3 py-1 border border-mist";
  } else {
    registerTab.className = "px-3 py-1 bg-sea text-white";
    loginTab.className = "px-3 py-1 border border-mist";
  }
}

jdInput.addEventListener("input", () => {
  jdCount.textContent = String(jdInput.value.length);
});

resumeInput.addEventListener("change", () => {
  sampleFile = null;
  const file = resumeInput.files?.[0];
  resumeName.textContent = file ? file.name : "";
});

document.getElementById("load-sample-btn").addEventListener("click", async () => {
  try {
    setStatus("loading", "Loading sample resume and job description…");
    const [jd, file] = await Promise.all([
      fetchSampleJobDescription(),
      fetchSampleResumeFile(),
    ]);
    jdInput.value = jd;
    jdCount.textContent = String(jd.length);
    sampleFile = file;
    resumeInput.value = "";
    resumeName.textContent = `${file.name} (sample)`;
    setStatus("", "");
  } catch (err) {
    setStatus("error", err.message || "Could not load samples.");
  }
});

document.getElementById("export-md-btn").addEventListener("click", () => {
  const analysis = getCurrentAnalysis();
  if (!analysis) return;
  downloadMarkdown(analysis);
});

document.getElementById("export-pdf-btn").addEventListener("click", () => {
  const analysis = getCurrentAnalysis();
  if (!analysis) return;
  try {
    exportPdfPrint(analysis);
  } catch (err) {
    setStatus("error", err.message);
  }
});

document.getElementById("auth-open-btn").addEventListener("click", () => {
  document.getElementById("auth-modal").classList.remove("hidden");
  document.getElementById("auth-error").classList.add("hidden");
});

document.getElementById("auth-close-btn").addEventListener("click", () => {
  document.getElementById("auth-modal").classList.add("hidden");
});

document.getElementById("tab-login").addEventListener("click", () => setAuthMode("login"));
document.getElementById("tab-register").addEventListener("click", () => setAuthMode("register"));

document.getElementById("logout-btn").addEventListener("click", async () => {
  await logout();
  currentUser = null;
  updateAuthBar();
  await refreshSavedHistory();
});

document.getElementById("auth-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const email = document.getElementById("auth-email").value.trim();
  const password = document.getElementById("auth-password").value;
  const errorEl = document.getElementById("auth-error");
  errorEl.classList.add("hidden");
  try {
    currentUser = authMode === "login" ? await login(email, password) : await register(email, password);
    document.getElementById("auth-modal").classList.add("hidden");
    updateAuthBar();
    await refreshSavedHistory();
  } catch (err) {
    errorEl.textContent = err.message || "Authentication failed.";
    errorEl.classList.remove("hidden");
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideResults();

  const file = sampleFile || resumeInput.files?.[0];
  const jobDescription = jdInput.value.trim();

  if (!file) {
    setStatus("error", "Please choose a PDF or DOCX resume.");
    return;
  }
  if (!jobDescription) {
    setStatus("error", "Please paste a job description.");
    return;
  }

  submitBtn.disabled = true;
  setStatus("loading", "Analyzing resume… this may take a few seconds.");

  try {
    const { analysis } = await analyzeResume(file, jobDescription);
    setStatus("", "");
    renderResults(analysis);
    addSessionHistoryItem(analysis, file.name, jobDescription);
    refreshSessionHistory();
    if (currentUser) {
      await refreshSavedHistory();
    }
  } catch (err) {
    setStatus("error", err.message || "Analysis failed. Please try again.");
  } finally {
    submitBtn.disabled = false;
  }
});

async function boot() {
  refreshSessionHistory();
  try {
    currentUser = await getMe();
  } catch {
    currentUser = null;
  }
  updateAuthBar();
  await refreshSavedHistory();
}

boot();
