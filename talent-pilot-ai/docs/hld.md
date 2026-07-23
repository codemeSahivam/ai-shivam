# TalentPilot AI

# High-Level Design (HLD)

**Project:** TalentPilot AI\
**Module:** Stage 1 -- AI Resume Reviewer\
**Version:** 1.0\
**Status:** Draft

------------------------------------------------------------------------

# 1. Introduction

## Purpose

This document describes the High-Level Design (HLD) for **TalentPilot AI
-- Stage 1: AI Resume Reviewer**.

The objective of this module is to allow users to upload a resume and
provide a job description, after which the system uses **Google Gemini**
to analyze the resume and generate structured hiring insights.

This document covers the overall architecture, technology stack, major
system components, request flow, deployment strategy, and future
scalability.

------------------------------------------------------------------------

# 2. Scope

## In Scope

-   Resume upload (PDF)
-   Resume text extraction
-   Job description input
-   AI-powered resume analysis
-   ATS-style scoring
-   Resume improvement suggestions
-   Responsive web interface
-   Local Docker deployment

## Out of Scope

-   Authentication & Authorization
-   Database
-   Resume history
-   Multi-user support
-   Admin portal
-   AI Agents
-   RAG
-   Vector databases
-   Interview scheduling

------------------------------------------------------------------------

# 3. Objectives

-   Learn AI application development through a real project.
-   Integrate Google Gemini with FastAPI.
-   Build a clean REST API.
-   Keep the application modular and maintainable.
-   Design an architecture that supports future enhancements.

------------------------------------------------------------------------

# 4. Technology Stack

  Layer              Technology
  ------------------ ----------------------------
  Frontend           HTML5 + Vanilla JavaScript
  Styling            Tailwind CSS
  Backend            FastAPI
  Validation         Pydantic
  Resume Parsing     PyMuPDF
  AI Provider        Google Gemini
  Database           None (Stage 1)
  Containerization   Docker
  Version Control    GitHub

------------------------------------------------------------------------

# 5. High-Level Architecture

``` text
+------------------------------------------------------+
|                    Web Browser                       |
+--------------------------+---------------------------+
                           |
                           | HTTP/HTTPS
                           v
+------------------------------------------------------+
| HTML + Tailwind CSS + Vanilla JavaScript             |
|------------------------------------------------------|
| Resume Upload                                        |
| Job Description Form                                 |
| Results Dashboard                                    |
+--------------------------+---------------------------+
                           |
                           | REST API
                           v
+------------------------------------------------------+
| FastAPI Backend                                      |
|------------------------------------------------------|
| API Routes                                           |
| Request Validation                                   |
| Resume Parser (PyMuPDF)                              |
| Prompt Builder                                       |
| Gemini Service                                       |
| Response Formatter                                   |
+--------------------------+---------------------------+
                           |
                           | HTTPS
                           v
+------------------------------------------------------+
| Google Gemini API                                    |
+------------------------------------------------------+
```

------------------------------------------------------------------------

# 6. Architecture Layers

## Presentation Layer

Responsibilities:

-   Resume upload
-   Job description input
-   Display AI analysis
-   Loading and error states

Technology:

-   HTML5
-   Tailwind CSS
-   Vanilla JavaScript

------------------------------------------------------------------------

## Application Layer

Responsibilities:

-   Request validation
-   Resume parsing
-   Prompt generation
-   AI integration
-   Response formatting
-   Error handling

Technology:

-   FastAPI
-   Pydantic
-   PyMuPDF

------------------------------------------------------------------------

## AI Layer

Responsibilities:

-   Resume evaluation
-   Skill extraction
-   ATS scoring
-   Resume summary
-   Recommendations

Technology:

-   Google Gemini

------------------------------------------------------------------------

# 7. Component Overview

``` text
Frontend
│
├── index.html
├── Upload Module
├── Results Module
├── API Client
└── UI Renderer

↓

FastAPI

├── API Router
├── Validation Layer
├── Resume Parser
├── Prompt Builder
├── Gemini Service
└── Response Mapper

↓

Google Gemini
```

------------------------------------------------------------------------

# 8. Request Flow

``` text
User

↓

Upload Resume

↓

Enter Job Description

↓

Click Analyze

↓

Frontend sends POST request

↓

FastAPI validates input

↓

PyMuPDF extracts text

↓

Prompt Builder creates AI prompt

↓

Google Gemini API

↓

Structured JSON Response

↓

Pydantic validates response

↓

Frontend renders analysis
```

------------------------------------------------------------------------

# 9. Functional Modules

## Frontend

-   Resume Upload
-   Job Description Input
-   API Integration
-   Loading Indicators
-   Result Rendering

## Resume Parser

-   Read PDF
-   Extract text
-   Normalize whitespace

## Prompt Builder

-   Combine resume and job description
-   Create structured prompt
-   Define expected JSON schema

## Gemini Service

-   Authenticate API requests
-   Send prompts
-   Receive responses
-   Handle retries and failures

## Response Mapper

-   Validate AI response
-   Transform response into frontend-friendly JSON

------------------------------------------------------------------------

# 10. Security Considerations

-   Validate uploaded files
-   Restrict file size
-   Accept supported MIME types only
-   Keep Gemini API key on the server
-   Store secrets in environment variables
-   Sanitize extracted text
-   Return generic error messages

------------------------------------------------------------------------

# 11. Error Handling

  Scenario                  Response
  ------------------------- ----------------------------
  Invalid file              HTTP 400
  Empty resume              HTTP 400
  Missing job description   HTTP 400
  Gemini timeout            HTTP 503
  Invalid AI response       HTTP 500
  Network failure           Retry then fail gracefully

------------------------------------------------------------------------

# 12. Deployment

``` text
Docker
│
├── Frontend Container
│     └── Static HTML/CSS/JS
│
└── Backend Container
      ├── FastAPI
      ├── PyMuPDF
      └── Gemini Client
```

Future stages can introduce Docker Compose, Kubernetes, PostgreSQL,
Redis, and background workers.

------------------------------------------------------------------------

# 13. Project Structure

``` text
talentpilot-ai/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   ├── assets/
│   └── Dockerfile
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── prompts/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── exceptions/
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── docs/
├── docker-compose.yml
├── .env.example
└── README.md
```

------------------------------------------------------------------------

# 14. Future Roadmap

``` text
Stage 1
Frontend
   ↓
FastAPI
   ↓
Gemini

Stage 2
+ PostgreSQL

Stage 3
+ RAG
+ Vector Database

Stage 4
+ AI Interviewer
+ Recruiter Dashboard

Stage 5
+ Multi-Agent System
```

------------------------------------------------------------------------

# 15. Risks

  Risk                Mitigation
  ------------------- -------------------------------------
  API rate limits     Retry and backoff
  Poor AI responses   Improve prompts and validate output
  Large PDFs          Enforce upload limits
  Invalid JSON        Validate using Pydantic

------------------------------------------------------------------------

# 16. Success Criteria

The implementation is successful when:

-   Resume upload works correctly.
-   Resume text is extracted accurately.
-   Google Gemini returns structured analysis.
-   Results are rendered successfully.
-   The application runs locally with Docker.
-   The architecture remains modular and extensible.

------------------------------------------------------------------------

# 17. Future Enhancements

-   Authentication
-   Resume history
-   PostgreSQL
-   Redis
-   AI Interview Assistant
-   Cover Letter Generator
-   RAG
-   AI Agents
-   Analytics Dashboard
-   Kubernetes deployment
-   CI/CD pipeline

------------------------------------------------------------------------

**End of Document**
