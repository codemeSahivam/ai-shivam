import {
  analyzeResume,
  fetchSampleJobDescription,
  fetchSampleResumeFile,
  fetchSavedHistory,
  getMe,
  login,
  logout,
  register,
} from "../services/api.js";
import { downloadMarkdown, exportPdfPrint } from "../services/export.js";
import {
  addSessionHistoryItem,
  getSessionHistory,
  renderHistoryList,
} from "../services/session-history.js";
import { getCurrentAnalysis, hideResults, renderResults } from "../components/results-panel.js";
import { MAX_JOB_DESCRIPTION_CHARS } from "../config.js";
import { initTheme } from "../utils/theme.js";

let currentUser = null;
let authMode = "login";
let sampleFile = null;

function setStatus(kind, message) {
  const statusEl = document.getElementById("status");
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
    listEl.replaceChildren();
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
  document.getElementById("tab-login").classList.toggle("active", mode === "login");
  document.getElementById("tab-register").classList.toggle("active", mode === "register");
}

export function bootApp() {
  initTheme();

  const form = document.getElementById("analyze-form");
  const submitBtn = document.getElementById("submit-btn");
  const jdInput = document.getElementById("job_description");
  const jdCount = document.getElementById("jd-count");
  const resumeInput = document.getElementById("resume");
  const resumeName = document.getElementById("resume-name");

  jdInput.addEventListener("input", () => {
    jdCount.textContent = String(jdInput.value.length);
  });

  resumeInput.addEventListener("change", () => {
    sampleFile = null;
    resumeName.textContent = resumeInput.files?.[0]?.name || "";
  });

  const fileDrop = document.getElementById("file-drop");
  if (fileDrop) {
    const setActive = (on) => fileDrop.classList.toggle("is-active", on);
    ["dragenter", "dragover"].forEach((evt) => {
      fileDrop.addEventListener(evt, (e) => {
        e.preventDefault();
        setActive(true);
      });
    });
    ["dragleave", "drop"].forEach((evt) => {
      fileDrop.addEventListener(evt, (e) => {
        e.preventDefault();
        setActive(false);
      });
    });
    fileDrop.addEventListener("drop", (e) => {
      const file = e.dataTransfer?.files?.[0];
      if (!file) return;
      sampleFile = null;
      const dt = new DataTransfer();
      dt.items.add(file);
      resumeInput.files = dt.files;
      resumeName.textContent = file.name;
    });
  }

  document.getElementById("load-sample-btn").addEventListener("click", async () => {
    try {
      setStatus("loading", "Loading sample resume and job description…");
      const [jd, file] = await Promise.all([
        fetchSampleJobDescription(),
        fetchSampleResumeFile(),
      ]);
      jdInput.value = jd.slice(0, MAX_JOB_DESCRIPTION_CHARS);
      jdCount.textContent = String(jdInput.value.length);
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
    if (analysis) downloadMarkdown(analysis);
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
      currentUser =
        authMode === "login" ? await login(email, password) : await register(email, password);
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
      if (currentUser) await refreshSavedHistory();
    } catch (err) {
      setStatus("error", err.message || "Analysis failed. Please try again.");
    } finally {
      submitBtn.disabled = false;
    }
  });

  refreshSessionHistory();
  getMe()
    .then(async (user) => {
      currentUser = user;
      updateAuthBar();
      await refreshSavedHistory();
    })
    .catch(() => {
      currentUser = null;
      updateAuthBar();
    });
}
