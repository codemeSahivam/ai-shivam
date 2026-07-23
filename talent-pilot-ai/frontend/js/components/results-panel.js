import { clearElement, createElement } from "../utils/dom.js";

let currentAnalysis = null;

const RECO_CLASS = {
  "Strong Hire": "reco-strong",
  Hire: "reco-hire",
  Consider: "reco-consider",
  Reject: "reco-reject",
};

export function getCurrentAnalysis() {
  return currentAnalysis;
}

function fillList(items, listEl) {
  clearElement(listEl);
  if (!items || items.length === 0) {
    listEl.appendChild(createElement("li", "empty-item", "None listed"));
    return;
  }
  for (const item of items) {
    listEl.appendChild(createElement("li", "", item));
  }
}

function fillChips(items, rowEl, tone) {
  clearElement(rowEl);
  if (!items || items.length === 0) {
    rowEl.appendChild(createElement("span", "chip chip-empty", "None listed"));
    return;
  }
  for (const item of items) {
    rowEl.appendChild(createElement("span", `chip chip-${tone}`, item));
  }
}

function fillSteps(items, listEl) {
  clearElement(listEl);
  if (!items || items.length === 0) {
    listEl.appendChild(createElement("li", "empty-item", "No suggestions yet."));
    return;
  }
  for (const item of items) {
    listEl.appendChild(createElement("li", "", item));
  }
}

function setRing(id, value) {
  const el = document.getElementById(id);
  if (!el) return;
  const pct = Math.max(0, Math.min(100, Number(value) || 0));
  el.style.setProperty("--p", String(pct));
}

function setRecommendation(value) {
  const text = value || "—";
  document.getElementById("recommendation").textContent = text;
  const banner = document.getElementById("reco-banner");
  if (!banner) return;
  banner.classList.remove("reco-strong", "reco-hire", "reco-consider", "reco-reject");
  banner.classList.add(RECO_CLASS[text] || "reco-consider");
}

export function renderResults(analysis) {
  currentAnalysis = analysis;
  const results = document.getElementById("results");
  results.classList.remove("hidden");
  results.classList.remove("reveal");
  void results.offsetWidth;
  results.classList.add("reveal");

  document.getElementById("match-score").textContent = `${analysis.match_score}`;
  document.getElementById("ats-score").textContent = `${analysis.ats_score}`;
  setRing("match-ring", analysis.match_score);
  setRing("ats-ring", analysis.ats_score);
  setRecommendation(analysis.recommendation);
  document.getElementById("summary").textContent = analysis.summary;
  fillList(analysis.match_score_breakdown || [], document.getElementById("match-breakdown"));
  fillList(analysis.ats_score_breakdown || [], document.getElementById("ats-breakdown"));
  fillChips(analysis.matching_skills, document.getElementById("matching-skills"), "good");
  fillChips(analysis.missing_skills, document.getElementById("missing-skills"), "warn");
  fillList(analysis.strengths, document.getElementById("strengths"));
  fillList(analysis.weaknesses, document.getElementById("weaknesses"));
  fillSteps(analysis.suggestions, document.getElementById("suggestions"));
  results.scrollIntoView({ behavior: "smooth", block: "start" });
}

export function hideResults() {
  const results = document.getElementById("results");
  results.classList.add("hidden");
  results.classList.remove("reveal");
  setRing("match-ring", 0);
  setRing("ats-ring", 0);
  document.getElementById("match-score").textContent = "—";
  document.getElementById("ats-score").textContent = "—";
  setRecommendation("—");
  currentAnalysis = null;
}
