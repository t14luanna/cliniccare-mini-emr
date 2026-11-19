def create(client, **overrides):
    body = {
        "patient_name": "Nguyen Van A",
        "notes": "Fever for 3 days.",
        "diagnosis_codes": ["A90"],
    }
    body.update(overrides)
    return client.post("/consultation", json=body)


def test_create_consultation(client):
    response = create(client, diagnosis_codes=["r50.9", "A90", "A90"])

    assert response.status_code == 201
    data = response.json()
    assert data["patient_name"] == "Nguyen Van A"
    assert data["doctor_name"] == "Dr. Demo"
    assert [d["code"] for d in data["diagnoses"]] == ["A90", "R50.9"]


def test_create_rejects_unknown_code(client):
    response = create(client, diagnosis_codes=["NOT-A-CODE"])
    assert response.status_code == 400
    assert "NOT-A-CODE" in response.json()["detail"]


def test_create_rejects_blank_fields(client):
    assert create(client, patient_name="   ").status_code == 422
    assert create(client, notes="").status_code == 422
    assert create(client, diagnosis_codes=[]).status_code == 422


def test_list_newest_first(client):
    create(client, patient_name="First Patient")
    create(client, patient_name="Second Patient")

    names = [c["patient_name"] for c in client.get("/consultation").json()]
    assert names == ["Second Patient", "First Patient"]


def test_filter_by_patient_and_diagnosis(client):
    create(client, patient_name="Nguyen Van A", diagnosis_codes=["A90"])
    create(client, patient_name="Tran Thi B", diagnosis_codes=["I10", "E11.9"])

    by_patient = client.get("/consultation", params={"patient": "tran"}).json()
    assert [c["patient_name"] for c in by_patient] == ["Tran Thi B"]

    by_code = client.get("/consultation", params={"diagnosis_code": "e11.9"}).json()
    assert [c["patient_name"] for c in by_code] == ["Tran Thi B"]

    nothing = client.get("/consultation", params={"diagnosis_code": "J00"}).json()
    assert nothing == []


def test_pagination(client):
    for i in range(3):
        create(client, patient_name=f"Patient {i}")

    first_page = client.get("/consultation", params={"limit": 2}).json()
    second_page = client.get("/consultation", params={"limit": 2, "offset": 2}).json()

    assert [c["patient_name"] for c in first_page] == ["Patient 2", "Patient 1"]
    assert [c["patient_name"] for c in second_page] == ["Patient 0"]
