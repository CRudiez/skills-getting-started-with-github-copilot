from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = f"{uuid4()}@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert unregister_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    activity_name = "Chess Club"
    email = f"missing-{uuid4()}@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 404
