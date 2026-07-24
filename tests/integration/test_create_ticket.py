from unittest.mock import AsyncMock
from uuid import uuid4
import pytest


def test_create_ticket_success(client, mock_db_session):
    payload = {
        "title": "Database connection error",
        "description": "Unable to connect to primary DB pool.",
        "priority": "high",
        "email": "user@example.com",
        "isOpen": True
    }

    response = client.post("/tickets/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 201
    assert data["message"] == "Ticket created successfully"
    assert "ticket_id" in data


def test_create_ticket_strips_title_whitespace(client, mock_db_session):
    payload = {
        "title": "  Database connection error  ",
        "description": "User cannot log in",
        "priority": "high",
        "email": "user@example.com",
        "isOpen": True
    }

    response = client.post("/tickets/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 201
    assert "ticket_id" in data


def test_create_ticket_validation_errors(client):
    res = client.post("/tickets/", json={"description": "No title", "email": "user@example.com"})
    assert res.status_code == 422

    res = client.post("/tickets/", json={"title": "No desc", "email": "user@example.com"})
    assert res.status_code == 422

    res = client.post("/tickets/", json={"title": "No email", "description": "Desc"})
    assert res.status_code == 422

    res = client.post(
        "/tickets/",
        json={"title": "T", "description": "D", "priority": "invalid_priority", "email": "user@example.com"}
    )
    assert res.status_code == 422
