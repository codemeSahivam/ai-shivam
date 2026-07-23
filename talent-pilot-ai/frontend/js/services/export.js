function analysisToMarkdown(analysis) {
  const list = (title, items) =>
    `## ${title}\n\n${(items || []).length ? items.map((i) => `- ${i}`).join("\n") : "- None"}\n`;
  return [
    `# TalentPilot AI — Resume Analysis`,
    ``,
    `**Overall match:** ${analysis.match_score}%`,
    `**ATS score:** ${analysis.ats_score} / 100`,
    `**Recommendation:** ${analysis.recommendation}`,
    ``,
    `## Summary`,
    ``,
    analysis.summary,
    ``,
    list("Match score breakdown", analysis.match_score_breakdown),
    list("ATS score breakdown", analysis.ats_score_breakdown),
    list("Matching skills", analysis.matching_skills),
    list("Missing skills", analysis.missing_skills),
    list("Strengths", analysis.strengths),
    list("Weaknesses", analysis.weaknesses),
    list("Suggestions", analysis.suggestions),
  ].join("\n");
}

export function downloadMarkdown(analysis, basename = "talentpilot-analysis") {
  const blob = new Blob([analysisToMarkdown(analysis)], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${basename}.md`;
  a.click();
  URL.revokeObjectURL(url);
}

export function exportPdfPrint(analysis) {
  const pre = document.createElement("pre");
  pre.textContent = analysisToMarkdown(analysis);
  const win = window.open("", "_blank");
  if (!win) throw new Error("Pop-up blocked. Allow pop-ups to export PDF.");
  win.document.title = "TalentPilot Analysis";
  const style = win.document.createElement("style");
  style.textContent = "body{font-family:Georgia,serif;padding:32px;line-height:1.5} pre{white-space:pre-wrap;font-family:inherit}";
  win.document.head.appendChild(style);
  win.document.body.appendChild(pre);
  win.focus();
  win.print();
}
