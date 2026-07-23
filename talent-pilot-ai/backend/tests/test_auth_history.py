from tests.conftest import make_pdf_bytes


def test_register_login_me_logout(client) -> None:
    register = client.post(
        "/api/v1/auth/register",
        json={"email": "jane@example.com", "password": "password123"},
    )
    assert register.status_code == 200
    assert register.json()["user"]["email"] == "jane@example.com"

    me = client.get("/api/v1/auth/me")
    assert me.status_code == 200

    logout = client.post("/api/v1/auth/logout")
    assert logout.status_code == 200

    me_after = client.get("/api/v1/auth/me")
    assert me_after.status_code == 401

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "jane@example.com", "password": "password123"},
    )
    assert login.status_code == 200


def test_analyze_saves_when_logged_in(client) -> None:
    client.post(
        "/api/v1/auth/register",
        json={"email": "saver@example.com", "password": "password123"},
    )
    pdf = make_pdf_bytes()
    response = client.post(
        "/api/v1/analyze",
        files={"resume": ("resume.pdf", pdf, "application/pdf")},
        data={"job_description": "Looking for a Python FastAPI engineer with Docker."},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["saved_id"] is not None

    history = client.get("/api/v1/history")
    assert history.status_code == 200
    items = history.json()["items"]
    assert len(items) == 1
    assert items[0]["match_score"] == 82

    detail = client.get(f"/api/v1/history/{items[0]['id']}")
    assert detail.status_code == 200
    assert detail.json()["recommendation"] == "Hire"


def test_history_requires_auth(client) -> None:
    response = client.get("/api/v1/history")
    assert response.status_code == 401


def test_history_not_found(client) -> None:
    client.post(
        "/api/v1/auth/register",
        json={"email": "missing@example.com", "password": "password123"},
    )
    response = client.get("/api/v1/history/9999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"
