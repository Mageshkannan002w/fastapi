import asyncio
from unittest.mock import Mock, AsyncMock
from uuid import UUID
import pytest

from app.services.ticket_service import TicketService
from app.schemas.ticket import TicketCreate
from app.models.ticket import Ticket


def test_create_ticket_success():
    mock_repo = AsyncMock()

    ticket_data = TicketCreate(
        title="Bug in login",
        description="User cannot log in",
        priority="high",
        isOpen=True,
        email="user@example.com"
    )

    mock_repo.create_ticket.side_effect = lambda ticket: ticket

    service = TicketService(mock_repo)

    result = asyncio.run(service.create_ticket(ticket_data))

    assert result.title == "Bug in login"
    assert result.description == "User cannot log in"
    assert result.priority == "high"
    assert result.isOpen is True
    assert result.email == "user@example.com"

    mock_repo.create_ticket.assert_called_once()
    created_arg = mock_repo.create_ticket.call_args[0][0]
    assert isinstance(created_arg, Ticket)
    assert created_arg.title == "Bug in login"


def test_create_ticket_generates_valid_uuid():
    mock_repo = AsyncMock()

    ticket_data = TicketCreate(
        title="UUID Test",
        description="Testing UUID generation",
        priority="medium",
        isOpen=True,
        email="test@example.com"
    )

    mock_repo.create_ticket.side_effect = lambda ticket: ticket

    service = TicketService(mock_repo)

    result = asyncio.run(service.create_ticket(ticket_data))

    assert result.id is not None
    uuid_obj = UUID(result.id)
    assert str(uuid_obj) == result.id


@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_create_ticket_priorities(priority):
    mock_repo = AsyncMock()

    ticket_data = TicketCreate(
        title=f"Priority {priority} issue",
        description=f"Description for {priority} priority",
        priority=priority,
        isOpen=True,
        email="user@example.com"
    )

    mock_repo.create_ticket.side_effect = lambda ticket: ticket

    service = TicketService(mock_repo)
    result = asyncio.run(service.create_ticket(ticket_data))

    assert result.priority == priority


@pytest.mark.parametrize("invalid_field,invalid_value,expected_error", [
    ("title", "", "Title cannot be empty"),
    ("title", "   ", "Title cannot be empty"),
    ("description", "", "Description cannot be empty"),
    ("description", "   ", "Description cannot be empty"),
    ("email", "", "Email cannot be empty"),
    ("email", "   ", "Email cannot be empty"),
])
def test_create_ticket_empty_or_whitespace_fields(invalid_field, invalid_value, expected_error):
    mock_repo = AsyncMock()

    ticket_data = Mock(spec=TicketCreate)
    ticket_data.title = "Valid Title"
    ticket_data.description = "Valid Description"
    ticket_data.email = "user@example.com"
    ticket_data.priority = "high"
    ticket_data.isOpen = True

    setattr(ticket_data, invalid_field, invalid_value)

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.create_ticket(ticket_data))

    assert str(exc_info.value) == expected_error
    mock_repo.create_ticket.assert_not_called()


def test_create_ticket_none_data():
    mock_repo = AsyncMock()
    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.create_ticket(None))

    assert str(exc_info.value) == "Ticket data is required"
    mock_repo.create_ticket.assert_not_called()


@pytest.mark.parametrize("is_open", [True, False])
def test_create_ticket_is_open_states(is_open):
    mock_repo = AsyncMock()

    ticket_data = TicketCreate(
        title="Ticket status test",
        description="Testing open status",
        priority="low",
        isOpen=is_open,
        email="user@example.com"
    )

    mock_repo.create_ticket.side_effect = lambda ticket: ticket

    service = TicketService(mock_repo)

    result = asyncio.run(service.create_ticket(ticket_data))

    assert result.isOpen is is_open


def test_create_ticket_repo_returns_none():
    mock_repo = AsyncMock()

    ticket_data = TicketCreate(
        title="Creation Failure",
        description="Testing repo returning None",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )

    mock_repo.create_ticket.return_value = None

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.create_ticket(ticket_data))

    assert str(exc_info.value) == "Failed to create ticket"
    mock_repo.create_ticket.assert_called_once()
