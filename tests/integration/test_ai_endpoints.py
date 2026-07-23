


def test_ai_summarize_endpoint_success(client):
    payload = {
        "ticket_description": "User is unable to log in due to invalid token error on dashboard."
    }

    response = client.post("/ai/summarize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "suggested_response" in data


def test_ai_summarize_endpoint_missing_payload(client):
    response = client.post("/ai/summarize", json={})
    assert response.status_code == 422


def test_ready_check_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
