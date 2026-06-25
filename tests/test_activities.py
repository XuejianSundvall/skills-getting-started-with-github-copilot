import urllib.parse

from src.app import activities


def quoted(name: str) -> str:
    return urllib.parse.quote(name, safe="")


def test_get_activities(client):
    # Arrange: none
    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "tester@example.com"
    assert email not in activities[activity]["participants"]

    # Act
    resp = client.post(f"/activities/{quoted(activity)}/signup?email={email}")

    # Assert
    assert resp.status_code == 200
    assert resp.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in activities[activity]["participants"]


def test_duplicate_signup_rejected(client):
    # Arrange: use an existing participant
    activity = "Chess Club"
    email = "michael@mergington.edu"
    assert email in activities[activity]["participants"]

    # Act
    resp = client.post(f"/activities/{quoted(activity)}/signup?email={email}")

    # Assert
    assert resp.status_code == 400
    assert "already" in resp.json().get("detail", "")


def test_capacity_enforced(client):
    # Arrange: set max_participants equal to current number of participants
    activity = "Tennis Club"
    participants = activities[activity]["participants"]
    activities[activity]["max_participants"] = len(participants)
    new_email = "capacity@test.com"

    # Act
    resp = client.post(f"/activities/{quoted(activity)}/signup?email={new_email}")

    # Assert
    assert resp.status_code == 400


def test_unregister_success(client):
    # Arrange
    activity = "Gym Class"
    email = "john@mergington.edu"
    assert email in activities[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{quoted(activity)}/signup?email={email}")

    # Assert
    assert resp.status_code == 200
    assert resp.json() == {"message": f"Unregistered {email} from {activity}"}
    assert email not in activities[activity]["participants"]


def test_unregister_not_signed_up(client):
    # Arrange
    activity = "Programming Class"
    email = "not.signedup@test.com"
    assert email not in activities[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{quoted(activity)}/signup?email={email}")

    # Assert
    assert resp.status_code == 400
    assert "not signed up" in resp.json().get("detail", "").lower()
