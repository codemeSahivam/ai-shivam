import { MAX_SESSION_ITEMS, SESSION_HISTORY_KEY } from "../config.js";
import { clearElement, createElement } from "../utils/dom.js";

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
  localStorage.setItem(SESSION_HISTORY_KEY, JSON.stringify(next));
  return next;
}

export function getSessionHistory() {
  try {
    const raw = localStorage.getItem(SESSION_HISTORY_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function renderHistoryList(listEl, items, onSelect) {
  clearElement(listEl);
  if (!items.length) {
    listEl.appendChild(createElement("p", "muted", "No analyses yet."));
    return;
  }
  for (const item of items) {
    const button = createElement("button", "history-item");
    button.type = "button";
    const row = createElement("div", "history-row");
    const name = createElement("span", "truncate", item.filename || "resume");
    const score = createElement("span", "history-score", `${item.match_score}%`);
    row.append(name, score);
    const preview = createElement("p", "muted truncate", item.job_description_preview || "");
    preview.style.margin = "0.25rem 0 0";
    const rec = createElement("p", "muted", item.recommendation || "");
    rec.style.margin = "0.25rem 0 0";
    button.append(row, preview, rec);
    button.addEventListener("click", () => onSelect(item));
    listEl.appendChild(button);
  }
}
