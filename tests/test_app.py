from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_for_activity_and_unregister_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: register a new participant
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: registration succeeds
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for {activity_name}"

    # Act: remove the participant
    delete_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert: removal succeeds
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Programming Class"
    email = "duplicate@mergington.edu"

    # Act
    first_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_signup = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_signup.status_code == 200
    assert second_signup.status_code == 400
    assert "already signed up" in second_signup.json()["detail"].lower()
