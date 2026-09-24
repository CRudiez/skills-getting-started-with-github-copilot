from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_participant_adds_email():
    # Arrange
    activity_name = "Chess Club"
    email = f"signup-{uuid4()}@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_duplicate_student_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_removes_email():
    # Arrange
    activity_name = "Chess Club"
    email = f"unregister-{uuid4()}@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    # Act
    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = f"missing-{uuid4()}@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
