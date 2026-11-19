def test_search_by_code(client):
    response = client.get("/diagnosis", params={"search": "e11"})
    assert response.status_code == 200
    codes = [item["code"] for item in response.json()]
    assert codes == ["E11.40", "E11.65", "E11.9"]


def test_search_by_description(client):
    response = client.get("/diagnosis", params={"search": "hypertension"})
    assert response.json() == [
        {"code": "I10", "description": "Essential (primary) hypertension"}
    ]


def test_search_respects_limit(client):
    response = client.get("/diagnosis", params={"limit": 5})
    assert len(response.json()) == 5


def test_search_rejects_invalid_limit(client):
    response = client.get("/diagnosis", params={"limit": 0})
    assert response.status_code == 422
