# TalentPilot AI

> **Stage 1 Product Requirements Document (PRD)**\
> **Module:** AI Resume Reviewer\
> **Version:** 1.0

------------------------------------------------------------------------

# 1. Project Overview

## Project Name

**TalentPilot AI**

### Vision

TalentPilot AI is an AI-powered recruitment and hiring platform designed
to streamline the hiring lifecycle using Large Language Models (LLMs).
The platform will evolve in multiple stages, starting with an AI-powered
Resume Reviewer and eventually expanding into a complete hiring
ecosystem featuring ATS scoring, AI interviews, candidate management,
recruiter dashboards, and AI agents.

------------------------------------------------------------------------

# 2. Stage 1 Overview

## Module

**AI Resume Reviewer**

### Goal

Build a web application where users upload a resume and provide a job
description. The application analyzes how well the resume matches the
job requirements using an LLM and presents actionable feedback.

### Learning Objectives

-   LLM API Integration
-   Prompt Engineering
-   FastAPI
-   Structured JSON Responses
-   Frontend ↔ Backend Communication

------------------------------------------------------------------------

# 3. Functional Requirements

## FR-1: Upload Resume

### Description

The system shall allow users to upload a resume.

### Supported Formats

-   PDF
-   DOCX *(Optional for Stage 1)*

### Maximum File Size

-   10 MB

### Validation

-   Reject unsupported file types.
-   Reject empty files.
-   Reject files larger than 10 MB.

------------------------------------------------------------------------

## FR-2: Job Description Input

### Description

The system shall allow users to paste a job description.

### Constraints

-   Maximum length: **10,000 characters**

### Validation

-   Resume is required.
-   Job Description is required.

------------------------------------------------------------------------

## FR-3: AI Analysis

When the user clicks **Analyze Resume**, the system shall:

1.  Extract resume text.
2.  Combine resume text with the job description.
3.  Send the prompt to the configured LLM.
4.  Receive a structured JSON response.
5.  Display the analysis.

------------------------------------------------------------------------

## FR-4: AI Analysis Output

The AI response shall include:

### Overall Match Score

Example:

``` text
82%
```

### Resume Summary

``` text
Strong backend engineer with Java, Python,
Docker and Kubernetes experience.
```

### Matching Skills

``` text
Spring Boot
FastAPI
Kafka
Docker
Kubernetes
PostgreSQL
```

### Missing Skills

``` text
Terraform
Redis
AWS Lambda
```

### Strengths

-   Strong backend experience
-   Cloud knowledge
-   Good project experience

### Weaknesses

-   No certifications
-   No quantified achievements
-   Missing testing experience

### Improvement Suggestions

``` text
Mention scalability achievements.

Add cloud projects.

Include measurable metrics.
```

### ATS Score

``` text
76 / 100
```

### Hiring Recommendation

Possible values:

-   Strong Hire
-   Hire
-   Consider
-   Reject

------------------------------------------------------------------------

## FR-5: Analysis History *(Optional)*

Display the last five resume analyses during the current session.

------------------------------------------------------------------------

# 4. Non-Functional Requirements

## Performance

-   API response time should generally remain below **10 seconds**
    *(excluding LLM latency)*.
-   Display a loading indicator while processing.

## Security

-   Validate uploaded files.
-   Enforce upload size limits.
-   Sanitize extracted text before sending it to the LLM.
-   Do not permanently store uploaded resumes in Stage 1.
-   Never expose API keys to the frontend.

## Reliability

Gracefully handle:

-   Invalid files
-   Empty resume
-   Empty job description
-   LLM failures
-   Network timeouts

------------------------------------------------------------------------

# 5. User Interface

## Home Screen

``` text
------------------------------------
TalentPilot AI
AI Resume Reviewer
------------------------------------

Upload Resume

[ Choose File ]

Job Description

______________________________
|                            |
|                            |
|                            |
|____________________________|

       Analyze Resume

------------------------------------

Results

Overall Score

ATS Score

Strengths

Weaknesses

Matching Skills

Missing Skills

Suggestions

Recommendation
```

------------------------------------------------------------------------

# 6. Technology Stack

## Frontend

-   Next.js (Recommended)
-   React (Alternative)

## Backend

-   FastAPI

## Database

-   None for Stage 1
-   In-memory processing only

## AI Provider

Supported Providers:

-   OpenAI *(Recommended)*
-   Gemini
-   Anthropic

## Resume Parsing

Recommended Library:

-   PyMuPDF

------------------------------------------------------------------------

# 7. REST API Specification

## Analyze Resume

### Endpoint

``` http
POST /api/v1/analyze
```

### Request

``` text
Content-Type: multipart/form-data

resume: File
job_description: String
```

### Success Response

``` json
{
  "success": true,
  "analysis": {
    "match_score": 82,
    "ats_score": 76,
    "summary": "...",
    "matching_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "recommendation": "Hire"
  }
}
```

### Error Response

``` json
{
  "success": false,
  "error": {
    "code": "INVALID_FILE",
    "message": "Only PDF files are supported."
  }
}
```

------------------------------------------------------------------------

# 8. Suggested Project Structure

``` text
talentpilot-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── prompts/
│   │   ├── utils/
│   │   ├── exceptions/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── types/
│   │
│   └── package.json
│
├── docs/
│
├── docker/
│
└── README.md
```

------------------------------------------------------------------------

# 9. Acceptance Criteria

The implementation shall be considered complete when:

-   Resume upload supports valid PDF files.
-   Job description input is validated.
-   Resume text is extracted successfully.
-   The LLM returns a structured JSON response.
-   Analysis is displayed correctly.
-   Invalid uploads produce meaningful error messages.
-   Loading and error states are handled gracefully.
-   API keys remain server-side.
-   The application can run locally (Docker Compose or separate
    frontend/backend execution).

------------------------------------------------------------------------

# 10. Deliverables Before Development

Before implementation, prepare:

1.  High-Level Design (HLD)
2.  Low-Level Design (LLD)
3.  Final Project Folder Structure
4.  OpenAPI Specification
5.  AI Response JSON Schema
6.  System Prompt for the LLM

------------------------------------------------------------------------

# 11. Review Process

Development should begin only after all design artifacts have been
reviewed and approved.

This project follows a professional engineering workflow:

``` text
Requirements
      ↓
High-Level Design (HLD)
      ↓
Low-Level Design (LLD)
      ↓
API Design
      ↓
Implementation
      ↓
Testing
      ↓
Review
      ↓
Deployment
```

------------------------------------------------------------------------

**End of Stage 1 PRD -- TalentPilot AI**
