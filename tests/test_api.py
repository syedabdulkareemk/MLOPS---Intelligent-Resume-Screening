import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to TalentLens MLOps API"}

def test_match_endpoint():
    response = client.post("/api/match?candidate_id=cand_1&job_id=job_1")
    assert response.status_code == 200
    data = response.json()
    assert "current_fit" in data
    assert data["candidate_id"] == "cand_1"
