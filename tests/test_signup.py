"""
Tests for the signup/unregister endpoints
"""

import pytest


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "test@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_nonexistent_activity(self, client):
        """Test signup for a non-existent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_participant(self, client):
        """Test that signing up twice for the same activity returns 400"""
        email = "duplicate@mergington.edu"
        
        # First signup should succeed
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second signup with same email should fail
        response2 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response2.status_code == 400
        data = response2.json()
        assert "already signed up" in data["detail"]

    def test_signup_missing_email_parameter(self, client):
        """Test signup without email parameter returns 422"""
        response = client.post("/activities/Chess Club/signup")
        assert response.status_code == 422

    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds the participant to the activity"""
        email = "verify@mergington.edu"
        
        # Sign up
        client.post("/activities/Programming Class/signup", params={"email": email})
        
        # Verify participant was added
        response = client.get("/activities")
        activities = response.json()
        assert email in activities["Programming Class"]["participants"]

    def test_signup_multiple_participants(self, client):
        """Test that multiple different participants can sign up for the same activity"""
        activity = "Art Studio"
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        
        for email in emails:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all participants were added
        response = client.get("/activities")
        activities = response.json()
        for email in emails:
            assert email in activities[activity]["participants"]


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""

    def test_unregister_success(self, client):
        """Test successful unregister from an activity"""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Removed" in data["message"]

    def test_unregister_nonexistent_activity(self, client):
        """Test unregister from a non-existent activity returns 404"""
        response = client.delete(
            "/activities/Nonexistent Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_participant_not_found(self, client):
        """Test unregister for a non-participant returns 404"""
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "notmember@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Participant not found" in data["detail"]

    def test_unregister_missing_email_parameter(self, client):
        """Test unregister without email parameter returns 422"""
        response = client.delete("/activities/Chess Club/signup")
        assert response.status_code == 422

    def test_unregister_removes_participant_from_activity(self, client):
        """Test that unregister actually removes the participant from activity"""
        email = "remove@mergington.edu"
        activity = "Basketball Team"
        
        # First, sign up
        client.post(f"/activities/{activity}/signup", params={"email": email})
        
        # Verify participant was added
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity]["participants"]
        
        # Now unregister
        client.delete(f"/activities/{activity}/signup", params={"email": email})
        
        # Verify participant was removed
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities[activity]["participants"]

    def test_signup_then_unregister_then_can_signup_again(self, client):
        """Test that a participant can sign up again after unregistering"""
        email = "rejoin@mergington.edu"
        activity = "Tennis Club"
        
        # Sign up
        response1 = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response1.status_code == 200
        
        # Unregister
        response2 = client.delete(f"/activities/{activity}/signup", params={"email": email})
        assert response2.status_code == 200
        
        # Sign up again should succeed
        response3 = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response3.status_code == 200
