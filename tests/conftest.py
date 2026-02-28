"""
Pytest configuration and shared fixtures for backend tests
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import the app
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from app import app as fastapi_app


@pytest.fixture
def client():
    """
    Fixture that provides a test client for the FastAPI application.
    The client can be used to make requests to the API in tests.
    """
    return TestClient(fastapi_app)


@pytest.fixture
def sample_activities():
    """
    Fixture that provides sample activity data for testing.
    Mirrors the structure of activities in the app.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
    }
