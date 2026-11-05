from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_activity_at_capacity_is_rejected():
    original_participants = activities["Programming Class"]["participants"][:]
    activities["Programming Class"]["participants"] = [
        f"student{i}@mergington.edu" for i in range(20)
    ]

    try:
        response = client.post(
            "/activities/Programming Class/signup?email=newstudent@mergington.edu"
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Activity is full"
    finally:
        activities["Programming Class"]["participants"] = original_participants
