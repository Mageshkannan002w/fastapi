from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_check_title_is_null():
    payload = {
        "title": None,
        "description": "This is a test ticket",
        "priority": "low",
    }

    response = client.post("tickets/", json=payload)
    assert response.status_code == 422
