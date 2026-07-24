import asyncio
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest

from app.services.ticket_service import TicketService
from app.schemas.ticket import TicketUpdateData
from app.models.ticket import Ticket


@pytest.mark.parametrize("update_data,expected_updates", [
    (TicketUpdateData(title="Updated Title"), {"title": "Updated Title"}),
    (TicketUpdateData(priority="high"), {"priority": "high"}),
    (TicketUpdateData(isOpen=False), {"isOpen": False}),
    (TicketUpdateData(description="New Desc"), {"description": "New Desc"}),
    (
        TicketUpdateData(title="New Title", description="New Desc", priority="high", isOpen=False),
        {"title": "New Title", "description": "New Desc", "priority": "high", "isOpen": False}
    ),
    (TicketUpdateData(), {}),
])
def test_update_ticket_fields(update_data, expected_updates):
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
        title=expected_updates.get("title", "Old Title"),
        description=expected_updates.get("description", "Old Desc"),
        priority=expected_updates.get("priority", "low"),
        isOpen=expected_updates.get("isOpen", True),
        email="user@example.com"
    )

    mock_repo.get_ticket_by_id.return_value = existing_ticket
    mock_repo.update_ticket.return_value = updated_ticket

    service = TicketService(mock_repo)

    result = asyncio.run(service.update_ticket(ticket_id, update_data))

    assert result == updated_ticket
    mock_repo.get_ticket_by_id.assert_called_once_with(ticket_id, None, None)
    mock_repo.update_ticket.assert_called_once_with(ticket_id, expected_updates)


@pytest.mark.parametrize("invalid_id,expected_error", [
    (None, "Ticket ID is required"),
])
def test_update_ticket_invalid_id(invalid_id, expected_error):
    mock_repo = AsyncMock()
    update_data = TicketUpdateData(title="Updated Title")

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.update_ticket(invalid_id, update_data))

    assert str(exc_info.value) == expected_error
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
