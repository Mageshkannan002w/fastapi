from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import pytest

from app.models.ticket import Ticket


def test_delete_ticket_success(client, mock_db_session):
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


def test_delete_ticket_validation_errors(client):
    response = client.delete("/tickets/delete")
    assert response.status_code == 422

    response = client.delete("/tickets/delete?ticket_id=12345")
    assert response.status_code == 422
