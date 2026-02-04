import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Soccer Team"
    # Remove if already present
    client.delete(f"/activities/{activity}/participant", params={"email": email})
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

def test_remove_participant():
    email = "removeuser@mergington.edu"
    activity = "Basketball Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/participant", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == "Participant was removed successfully"
    # Removing again should fail
    response2 = client.delete(f"/activities/{activity}/participant", params={"email": email})
    assert response2.status_code == 404
    assert "Participant not found" in response2.json()["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_remove_participant_activity_not_found():
    response = client.delete("/activities/Nonexistent/participant", params={"email": "ghost@mergington.edu"})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
