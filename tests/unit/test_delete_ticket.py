import asyncio
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
import pytest

from app.services.ticket_service import TicketService
from app.models.ticket import Ticket


def test_delete_ticket_success():
    mock_repo = Mock()
    ticket_id = uuid4()

    existing_ticket = Ticket(
        id=str(ticket_id),
        title="To Delete",
        description="Desc",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    mock_repo.get_ticket_by_id = AsyncMock(return_value=existing_ticket)
    mock_repo.delete_ticket = AsyncMock(return_value=True)

    service = TicketService(mock_repo)

    result = asyncio.run(service.delete_ticket(ticket_id))

    assert result is True
    mock_repo.get_ticket_by_id.assert_called_once_with(ticket_id, None, None)
    mock_repo.delete_ticket.assert_called_once_with(ticket_id)


def test_delete_ticket_none_id():
    mock_repo = Mock()
    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.delete_ticket(None))

    assert str(exc_info.value) == "Ticket ID is required"
    mock_repo.get_ticket_by_id.assert_not_called()
    mock_repo.delete_ticket.assert_not_called()


def test_delete_ticket_not_found():
    mock_repo = Mock()
    ticket_id = uuid4()

    mock_repo.get_ticket_by_id = AsyncMock(return_value=None)

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.delete_ticket(ticket_id))

    assert str(exc_info.value) == "Ticket not found"
    mock_repo.get_ticket_by_id.assert_called_once_with(ticket_id, None, None)
    mock_repo.delete_ticket.assert_not_called()


def test_delete_ticket_repo_failure():
    mock_repo = Mock()
    ticket_id = uuid4()

    existing_ticket = Ticket(
        id=str(ticket_id),
        title="To Delete",
        description="Desc",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    mock_repo.get_ticket_by_id = AsyncMock(return_value=existing_ticket)
    mock_repo.delete_ticket = AsyncMock(return_value=False)

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.delete_ticket(ticket_id))

    assert str(exc_info.value) == "An Error Occurred"
    mock_repo.get_ticket_by_id.assert_called_once_with(ticket_id, None, None)
    mock_repo.delete_ticket.assert_called_once_with(ticket_id)
