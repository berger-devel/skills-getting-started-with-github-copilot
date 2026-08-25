from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_data():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_for_activity_adds_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert email in activity["participants"]

    client.delete(f"/activities/{activity_name}/unregister?email={email}")


def test_duplicate_signup_is_rejected():
    activity_name = "Programming Class"
    email = "duplicate@mergington.edu"

    first_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_signup = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert first_signup.status_code == 200
    assert second_signup.status_code == 400
    assert "already signed up" in second_signup.json()["detail"].lower()

    client.delete(f"/activities/{activity_name}/unregister?email={email}")


def test_unregister_removes_participant():
    activity_name = "Gym Class"
    email = "leavingstudent@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]


def test_unregister_missing_participant_returns_404():
    response = client.delete("/activities/Chess Club/unregister?email=missing@mergington.edu")

    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"].lower()
