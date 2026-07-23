# Prompt Design

System and user prompts live in `backend/app/prompts/__init__.py`.

## Goals

- Force strict JSON matching the analysis schema
- Include match/ATS score breakdowns
- Prefer evidence from the resume; avoid invented credentials

## Response fields

`match_score`, `ats_score`, `match_score_breakdown`, `ats_score_breakdown`, `summary`, `matching_skills`, `missing_skills`, `strengths`, `weaknesses`, `suggestions`, `recommendation`

See [ai-response-schema.json](ai-response-schema.json) and [system-prompt.md](system-prompt.md).
