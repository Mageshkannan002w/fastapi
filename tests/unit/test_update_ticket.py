import asyncio
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest

from app.services.ticket_service import TicketService
from app.schemas.ticket import TicketUpdateData
from app.models.ticket import Ticket


def test_update_ticket_success():
    mock_repo = AsyncMock()
    ticket_id = uuid4()

    existing_ticket = Ticket(
        id=str(ticket_id),
        title="Old Title",
        description="Old Desc",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    updated_ticket = Ticket(
        id=str(ticket_id),
        title="Updated Title",
        description="Old Desc",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    update_data = TicketUpdateData(title="Updated Title")

    mock_repo.get_ticket_by_id.return_value = existing_ticket
    mock_repo.update_ticket.return_value = updated_ticket

    service = TicketService(mock_repo)

    result = asyncio.run(service.update_ticket(ticket_id, update_data))

    assert result == updated_ticket
    assert result.title == "Updated Title"
    mock_repo.get_ticket_by_id.assert_called_once_with(ticket_id, None, None)
    mock_repo.update_ticket.assert_called_once_with(ticket_id, {"title": "Updated Title"})


def test_update_ticket_missing_ticket_id():
    mock_repo = AsyncMock()
    update_data = TicketUpdateData(title="Updated Title")

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.update_ticket(None, update_data))

    assert str(exc_info.value) == "Ticket ID is required"
    mock_repo.get_ticket_by_id.assert_not_called()
    mock_repo.update_ticket.assert_not_called()


def test_update_ticket_wrong_id_not_found():
    mock_repo = AsyncMock()
    wrong_ticket_id = uuid4()
    update_data = TicketUpdateData(title="Updated Title")

    mock_repo.get_ticket_by_id.return_value = None

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.update_ticket(wrong_ticket_id, update_data))

    assert str(exc_info.value) == "Ticket not found"
    mock_repo.get_ticket_by_id.assert_called_once_with(wrong_ticket_id, None, None)
    mock_repo.update_ticket.assert_not_called()


def test_update_ticket_priority_change():
    mock_repo = AsyncMock()
    ticket_id = uuid4()

    existing_ticket = Ticket(
        id=str(ticket_id),
        title="Title",
        description="Desc",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    updated_ticket = Ticket(
        id=str(ticket_id),
        title="Title",
        description="Desc",
        priority="high",
        isOpen=True,
        email="user@example.com"
    )

    update_data = TicketUpdateData(priority="high")

    mock_repo.get_ticket_by_id.return_value = existing_ticket
    mock_repo.update_ticket.return_value = updated_ticket

    service = TicketService(mock_repo)

    result = asyncio.run(service.update_ticket(ticket_id, update_data))

    assert result.priority == "high"
    mock_repo.update_ticket.assert_called_once_with(ticket_id, {"priority": "high"})


def test_update_ticket_multiple_fields():
    mock_repo = AsyncMock()
    ticket_id = uuid4()

    existing_ticket = Ticket(
        id=str(ticket_id),
        title="Old Title",
        description="Old Desc",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    updated_ticket = Ticket(
        id=str(ticket_id),
        title="New Title",
        description="New Desc",
        priority="high",
        isOpen=False,
        email="user@example.com"
    )

    update_data = TicketUpdateData(
        title="New Title",
        description="New Desc",
        priority="high",
        isOpen=False
    )

    mock_repo.get_ticket_by_id.return_value = existing_ticket
    mock_repo.update_ticket.return_value = updated_ticket

    service = TicketService(mock_repo)

    result = asyncio.run(service.update_ticket(ticket_id, update_data))

    assert result == updated_ticket
    assert result.title == "New Title"
    assert result.priority == "high"
    assert result.isOpen is False
    mock_repo.get_ticket_by_id.assert_called_once_with(ticket_id, None, None)
    mock_repo.update_ticket.assert_called_once_with(
        ticket_id,
        {"title": "New Title", "description": "New Desc", "priority": "high", "isOpen": False}
    )


def test_update_ticket_partial_fields():
    mock_repo = AsyncMock()
    ticket_id = uuid4()

    existing_ticket = Ticket(
        id=str(ticket_id),
        title="Title",
        description="Desc",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    updated_ticket = Ticket(
        id=str(ticket_id),
        title="Title",
        description="Desc",
        priority="low",
        isOpen=False,
        email="user@example.com"
    )

    update_data = TicketUpdateData(isOpen=False)

    mock_repo.get_ticket_by_id.return_value = existing_ticket
    mock_repo.update_ticket.return_value = updated_ticket

    service = TicketService(mock_repo)

    result = asyncio.run(service.update_ticket(ticket_id, update_data))

    assert result.isOpen is False
    mock_repo.update_ticket.assert_called_once_with(ticket_id, {"isOpen": False})


def test_update_ticket_empty_payload():
    mock_repo = AsyncMock()
    ticket_id = uuid4()

    existing_ticket = Ticket(
        id=str(ticket_id),
        title="Title",
        description="Desc",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    update_data = TicketUpdateData()

    mock_repo.get_ticket_by_id.return_value = existing_ticket
    mock_repo.update_ticket.return_value = existing_ticket

    service = TicketService(mock_repo)

    result = asyncio.run(service.update_ticket(ticket_id, update_data))

    assert result == existing_ticket
    mock_repo.update_ticket.assert_called_once_with(ticket_id, {})
