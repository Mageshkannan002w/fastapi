from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import pytest

from app.models.ticket import Ticket


def test_get_tickets_success(client, mock_db_session):
    mock_ticket = Ticket(
        id=str(uuid4()),
        title="Database connection error",
        description="Sample Desc",
        priority="high",
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
    assert data["ticket"] is not None


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


def test_get_tickets_invalid_query_params(client):
    response = client.get("/tickets/get_tickets?isOpen=not_a_bool")
    assert response.status_code == 422
