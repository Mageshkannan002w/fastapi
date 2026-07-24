import asyncio
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
import pytest

from app.services.ticket_service import TicketService
from app.models.ticket import Ticket


def test_get_ticket_by_id():
    mock_repo = Mock()
    ticket_id = uuid4()
    mock_ticket = Ticket(
        id=str(ticket_id),
        title="Test Ticket",
        description="Test Description",
        priority="high",
        isOpen=True,
        email="test@example.com"
    )
    mock_repo.get_ticket_by_id = AsyncMock(return_value=mock_ticket)

    service = TicketService(mock_repo)

    result = asyncio.run(service.get_ticket(ticket_id=ticket_id))

    assert result == mock_ticket
    assert result.title == "Test Ticket"
    mock_repo.get_ticket_by_id.assert_called_once_with(ticket_id)


def test_get_ticket_by_id_not_found():
    mock_repo = Mock()
    ticket_id = uuid4()
    mock_repo.get_ticket_by_id = AsyncMock(return_value=None)

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.get_ticket(ticket_id=ticket_id))

    assert str(exc_info.value) == "Ticket not found"
    mock_repo.get_ticket_by_id.assert_called_once_with(ticket_id)


@pytest.mark.parametrize("mismatched_kwargs", [
    {"priority": "high"},
    {"isOpen": False},
    {"priority": "high", "isOpen": False},
])
def test_get_ticket_by_id_attribute_mismatch(mismatched_kwargs):
    mock_repo = Mock()
    ticket_id = uuid4()
    mock_ticket = Ticket(
        id=str(ticket_id),
        title="Test Ticket",
        description="Test Description",
        priority="low",
        isOpen=True,
        email="test@example.com"
    )
    mock_repo.get_ticket_by_id = AsyncMock(return_value=mock_ticket)

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.get_ticket(ticket_id=ticket_id, **mismatched_kwargs))

    assert str(exc_info.value) == "Ticket not found"


@pytest.mark.parametrize("priority_param,is_open_param", [
    ("high", True),
    ("low", False),
    ("medium", True),
])
def test_get_ticket_by_id_matching_filters(priority_param, is_open_param):
    mock_repo = Mock()
    ticket_id = uuid4()
    mock_ticket = Ticket(
        id=str(ticket_id),
        title="Matched Ticket",
        description="Desc",
        priority=priority_param,
        isOpen=is_open_param,
        email="user@example.com"
    )
    mock_repo.get_ticket_by_id = AsyncMock(return_value=mock_ticket)

    service = TicketService(mock_repo)

    result = asyncio.run(service.get_ticket(
        ticket_id=ticket_id,
        priority=priority_param,
        isOpen=is_open_param
    ))

    assert result == mock_ticket
    assert result.priority == priority_param
    assert result.isOpen is is_open_param


@pytest.mark.parametrize("filter_kwargs", [
    {},
    {"priority": "high"},
    {"isOpen": True},
    {"priority": "low", "isOpen": False},
])
def test_get_tickets_filters(filter_kwargs):
    mock_repo = Mock()
    mock_ticket = Ticket(
        id=str(uuid4()),
        title="Sample Ticket",
        description="Desc",
        priority=filter_kwargs.get("priority", "low"),
        isOpen=filter_kwargs.get("isOpen", True),
        email="user@example.com"
    )
    mock_repo.get_all_tickets = AsyncMock(return_value=[mock_ticket])

    service = TicketService(mock_repo)

    result = asyncio.run(service.get_ticket(**filter_kwargs))

    assert len(result) >= 1
    assert result[0] == mock_ticket
    mock_repo.get_all_tickets.assert_called_with(
        priority=filter_kwargs.get("priority"),
        isOpen=filter_kwargs.get("isOpen")
    )


def test_get_tickets_empty_list():
    mock_repo = Mock()
    mock_repo.get_all_tickets = AsyncMock(return_value=[])

    service = TicketService(mock_repo)

    result = asyncio.run(service.get_ticket())

    assert result == []
    mock_repo.get_all_tickets.assert_called_once_with(priority=None, isOpen=None)
