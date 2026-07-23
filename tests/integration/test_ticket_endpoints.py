from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import pytest

from app.models.ticket import Ticket


def test_create_ticket_endpoint_success(client, mock_db_session):
    payload = {
        "title": "Bug in login",
        "description": "User cannot log in",
        "priority": "high",
        "isOpen": True,
        "email": "user@example.com"
    }

    response = client.post("/tickets/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 201
    assert data["message"] == "Ticket created successfully"
    assert "ticket_id" in data


def test_create_ticket_endpoint_validation_errors(client):
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


def test_get_tickets_endpoint_success(client, mock_db_session):
    mock_ticket = Ticket(
        id=str(uuid4()),
        title="Sample Ticket",
        description="Sample Desc",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_ticket]
    mock_result.scalar_one_or_none.return_value = mock_ticket
    mock_db_session.execute = AsyncMock(return_value=mock_result)

    response = client.get("/tickets/get_tickets")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["message"] == "Tickets found successfully"


def test_get_ticket_by_id_not_found(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db_session.execute = AsyncMock(return_value=mock_result)

    ticket_id = str(uuid4())
    response = client.get(f"/tickets/get_tickets?ticket_id={ticket_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 404
    assert data["message"] == "Ticket not found"
    assert data["ticket"] is None


def test_get_tickets_endpoint_invalid_query_params(client):
    response = client.get("/tickets/get_tickets?isOpen=not_a_bool")
    assert response.status_code == 422


def test_update_ticket_endpoint_success(client, mock_db_session):
    ticket_id = str(uuid4())
    mock_ticket = Ticket(
        id=ticket_id,
        title="Old Title",
        description="Desc",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_ticket
    mock_db_session.execute = AsyncMock(return_value=mock_result)

    payload = {"title": "Updated Title"}
    response = client.put(f"/tickets/update?ticket_id={ticket_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["message"] == "Ticket updated successfully"


def test_update_ticket_endpoint_validation_errors(client):
    response = client.put("/tickets/update", json={"title": "Updated Title"})
    assert response.status_code == 422

    ticket_id = str(uuid4())
    response = client.put(f"/tickets/update?ticket_id={ticket_id}", json={"priority": "invalid_priority"})
    assert response.status_code == 422


def test_delete_ticket_endpoint_success(client, mock_db_session):
    ticket_id = str(uuid4())
    mock_ticket = Ticket(
        id=ticket_id,
        title="Delete Me",
        description="Desc",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_ticket
    mock_db_session.execute = AsyncMock(return_value=mock_result)

    response = client.delete(f"/tickets/delete?ticket_id={ticket_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["message"] == "Ticket deleted successfully"


def test_delete_ticket_endpoint_validation_errors(client):
    response = client.delete("/tickets/delete")
    assert response.status_code == 422

    response = client.delete("/tickets/delete?ticket_id=12345")
    assert response.status_code == 422
