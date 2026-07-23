const STORAGE_KEY = "talentpilot_session_history_v1";
const MAX_SESSION_ITEMS = 5;

/**
 * @param {object} analysis
 * @param {string} filename
 * @param {string} jobDescription
 */
export function addSessionHistoryItem(analysis, filename, jobDescription) {
  const items = getSessionHistory();
  const entry = {
    id: `local-${Date.now()}`,
    filename: filename || "resume",
    job_description_preview: (jobDescription || "").trim().slice(0, 120),
    match_score: analysis.match_score,
    ats_score: analysis.ats_score,
    recommendation: analysis.recommendation,
    created_at: new Date().toISOString(),
    analysis,
  };
  const next = [entry, ...items].slice(0, MAX_SESSION_ITEMS);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  return next;
}

export function getSessionHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

/**
 * @param {HTMLElement} listEl
 * @param {Array} items
 * @param {(item: object) => void} onSelect
 */
export function renderHistoryList(listEl, items, onSelect) {
  listEl.innerHTML = "";
  if (!items.length) {
    const empty = document.createElement("p");
    empty.className = "text-sm text-slate-500";
    empty.textContent = "No analyses yet.";
    listEl.appendChild(empty);
    return;
  }

  for (const item of items) {
    const button = document.createElement("button");
    button.type = "button";
    button.className =
      "w-full text-left border border-mist px-3 py-3 hover:bg-white/80 transition";
    button.innerHTML = `
      <div class="flex justify-between gap-3 text-sm">
        <span class="font-medium truncate">${escapeHtml(item.filename || "resume")}</span>
        <span class="text-sea shrink-0">${item.match_score}%</span>
      </div>
      <p class="mt-1 text-xs text-slate-500 truncate">${escapeHtml(item.job_description_preview || "")}</p>
      <p class="mt-1 text-xs text-slate-400">${escapeHtml(item.recommendation || "")}</p>
    `;
    button.addEventListener("click", () => onSelect(item));
    listEl.appendChild(button);
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}
