import pytest
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_check_title_type():
    payload = {
        "title": 123,
        "description": "This is a test ticket",
        "priority": "low",
    }
    with pytest.raises(ValueError):
        client.post("/tickets/", json=payload)     