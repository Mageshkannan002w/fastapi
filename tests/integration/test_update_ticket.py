from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import pytest

from app.models.ticket import Ticket


def test_update_ticket_success(client, mock_db_session):
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


def test_update_ticket_validation_errors(client):
    response = client.put("/tickets/update", json={"title": "Updated Title"})
    assert response.status_code == 422

    ticket_id = str(uuid4())
    response = client.put(f"/tickets/update?ticket_id={ticket_id}", json={"priority": "invalid_priority"})
    assert response.status_code == 422
