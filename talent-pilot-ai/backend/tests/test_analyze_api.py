from tests.conftest import make_pdf_bytes


def test_health(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_success(client) -> None:
    pdf = make_pdf_bytes()
    response = client.post(
        "/api/v1/analyze",
        files={"resume": ("resume.pdf", pdf, "application/pdf")},
        data={"job_description": "Looking for a Python FastAPI engineer with Docker."},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["analysis"]["match_score"] == 82
    assert body["analysis"]["recommendation"] == "Hire"
    assert body["analysis"]["match_score_breakdown"]
    assert body["saved_id"] is None


def test_analyze_missing_job_description(client) -> None:
    pdf = make_pdf_bytes()
    response = client.post(
        "/api/v1/analyze",
        files={"resume": ("resume.pdf", pdf, "application/pdf")},
        data={"job_description": "   "},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "MISSING_JOB_DESCRIPTION"


def test_analyze_invalid_file_type(client) -> None:
    response = client.post(
        "/api/v1/analyze",
        files={"resume": ("resume.txt", b"not a pdf", "text/plain")},
        data={"job_description": "Backend role"},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_FILE"


def test_analyze_empty_file(client) -> None:
    response = client.post(
        "/api/v1/analyze",
        files={"resume": ("resume.pdf", b"", "application/pdf")},
        data={"job_description": "Backend role"},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "EMPTY_FILE"


def test_sample_job_description(client) -> None:
    response = client.get("/api/v1/samples/job-description")
    assert response.status_code == 200
    assert "FastAPI" in response.json()["job_description"]


def test_sample_resume(client) -> None:
    response = client.get("/api/v1/samples/resume")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")


def test_ui_index(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert b"TalentPilot AI" in response.content
