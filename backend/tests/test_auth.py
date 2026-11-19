def test_login_success(anonymous_client):
    response = anonymous_client.post(
        "/auth/login", json={"username": "doctor", "password": "doctor123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["doctor"] == {"username": "doctor", "full_name": "Dr. Demo"}


def test_login_wrong_password(anonymous_client):
    response = anonymous_client.post(
        "/auth/login", json={"username": "doctor", "password": "wrong"}
    )
    assert response.status_code == 401


def test_protected_endpoints_need_token(anonymous_client):
    assert anonymous_client.get("/diagnosis").status_code == 401
    assert anonymous_client.get("/consultation").status_code == 401
    assert anonymous_client.post("/consultation", json={}).status_code == 401


def test_invalid_token_is_rejected(anonymous_client):
    anonymous_client.headers["Authorization"] = "Bearer not-a-real-token"
    assert anonymous_client.get("/consultation").status_code == 401


def test_me_returns_logged_in_doctor(client):
    assert client.get("/auth/me").json()["username"] == "doctor"
