/**
 * @param {string[]} items
 * @param {HTMLUListElement} listEl
 */
function fillList(items, listEl) {
  listEl.innerHTML = "";
  if (!items || items.length === 0) {
    const li = document.createElement("li");
    li.textContent = "None";
    li.className = "list-none text-slate-500";
    listEl.appendChild(li);
    return;
  }
  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = item;
    listEl.appendChild(li);
  }
}

let currentAnalysis = null;

export function getCurrentAnalysis() {
  return currentAnalysis;
}

/**
 * @param {object} analysis
 */
export function renderResults(analysis) {
  currentAnalysis = analysis;
  const results = document.getElementById("results");
  results.classList.remove("hidden");

  document.getElementById("match-score").textContent = `${analysis.match_score}%`;
  document.getElementById("ats-score").textContent = `${analysis.ats_score} / 100`;
  document.getElementById("recommendation").textContent = analysis.recommendation;
  document.getElementById("summary").textContent = analysis.summary;

  fillList(analysis.match_score_breakdown || [], document.getElementById("match-breakdown"));
  fillList(analysis.ats_score_breakdown || [], document.getElementById("ats-breakdown"));
  fillList(analysis.matching_skills, document.getElementById("matching-skills"));
  fillList(analysis.missing_skills, document.getElementById("missing-skills"));
  fillList(analysis.strengths, document.getElementById("strengths"));
  fillList(analysis.weaknesses, document.getElementById("weaknesses"));
  fillList(analysis.suggestions, document.getElementById("suggestions"));

  results.scrollIntoView({ behavior: "smooth", block: "start" });
}

export function hideResults() {
  document.getElementById("results").classList.add("hidden");
  currentAnalysis = null;
}
