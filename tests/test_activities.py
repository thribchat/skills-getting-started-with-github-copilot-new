"""
Tests for the activities endpoints
"""

import pytest


def test_get_activities_returns_success(client):
    """Test that GET /activities returns a 200 status code"""
    response = client.get("/activities")
    assert response.status_code == 200


def test_get_activities_returns_dict(client):
    """Test that GET /activities returns a dictionary"""
    response = client.get("/activities")
    data = response.json()
    assert isinstance(data, dict)


def test_get_activities_contains_expected_activities(client):
    """Test that GET /activities returns all expected activities"""
    response = client.get("/activities")
    data = response.json()
    
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Art Studio", "Drama Club", "Debate Team", "Science Club"
    ]
    
    for activity in expected_activities:
        assert activity in data


def test_activity_has_required_fields(client):
    """Test that each activity has the required fields"""
    response = client.get("/activities")
    data = response.json()
    
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_data in data.items():
        for field in required_fields:
            assert field in activity_data, f"Activity {activity_name} missing field {field}"


def test_activity_participants_is_list(client):
    """Test that participants field is a list for all activities"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data["participants"], list), \
            f"Participants for {activity_name} is not a list"


def test_activity_max_participants_is_positive_int(client):
    """Test that max_participants is a positive integer"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data["max_participants"], int), \
            f"max_participants for {activity_name} is not an integer"
        assert activity_data["max_participants"] > 0, \
            f"max_participants for {activity_name} is not positive"
