/**
 * @param {object} analysis
 */
export function analysisToMarkdown(analysis) {
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

/**
 * @param {object} analysis
 * @param {string} [basename]
 */
export function downloadMarkdown(analysis, basename = "talentpilot-analysis") {
  const markdown = analysisToMarkdown(analysis);
  const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${basename}.md`;
  a.click();
  URL.revokeObjectURL(url);
}

/**
 * @param {object} analysis
 */
export function exportPdfPrint(analysis) {
  const markdown = analysisToMarkdown(analysis)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;");
  const html = `<!DOCTYPE html>
<html><head><title>TalentPilot Analysis</title>
<style>
  body { font-family: Georgia, serif; padding: 32px; color: #0f172a; line-height: 1.5; }
  pre { white-space: pre-wrap; font-family: inherit; }
</style></head>
<body><pre>${markdown}</pre>
<script>window.onload = () => { window.print(); }</script>
</body></html>`;
  const win = window.open("", "_blank");
  if (!win) {
    throw new Error("Pop-up blocked. Allow pop-ups to export PDF.");
  }
  win.document.write(html);
  win.document.close();
}
