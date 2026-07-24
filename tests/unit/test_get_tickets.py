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
    mock_repo.get_ticket_by_id.assert_called_once_with(ticket_id, None, None)


def test_get_ticket_by_id_not_found():
    mock_repo = Mock()
    ticket_id = uuid4()
    mock_repo.get_ticket_by_id = AsyncMock(return_value=None)

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.get_ticket(ticket_id=ticket_id))

    assert str(exc_info.value) == "Ticket not found"
    mock_repo.get_ticket_by_id.assert_called_once_with(ticket_id, None, None)


def test_get_ticket_by_id_priority_mismatch():
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
        asyncio.run(service.get_ticket(ticket_id=ticket_id, priority="high"))

    assert str(exc_info.value) == "Ticket not found"


def test_get_ticket_by_id_is_open_mismatch():
    mock_repo = Mock()
    ticket_id = uuid4()
    mock_ticket = Ticket(
        id=str(ticket_id),
        title="Test Ticket",
        description="Test Description",
        priority="low",
        isOpen=False,
        email="test@example.com"
    )
    mock_repo.get_ticket_by_id = AsyncMock(return_value=mock_ticket)

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.get_ticket(ticket_id=ticket_id, isOpen=True))

    assert str(exc_info.value) == "Ticket not found"


def test_get_ticket_by_id_matching_priority_and_is_open():
    mock_repo = Mock()
    ticket_id = uuid4()
    mock_ticket = Ticket(
        id=str(ticket_id),
        title="Matched Ticket",
        description="Desc",
        priority="high",
        isOpen=True,
        email="user@example.com"
    )
    mock_repo.get_ticket_by_id = AsyncMock(return_value=mock_ticket)

    service = TicketService(mock_repo)

    result = asyncio.run(service.get_ticket(ticket_id=ticket_id, priority="high", isOpen=True))

    assert result == mock_ticket
    assert result.priority == "high"
    assert result.isOpen is True


def test_get_all_tickets():
    mock_repo = Mock()
    mock_ticket = Ticket(
        id=str(uuid4()),
        title="Ticket 1",
        description="Desc 1",
        priority="low",
        isOpen=True,
        email="user@example.com"
    )
    mock_repo.get_all_tickets = AsyncMock(return_value=[mock_ticket])

    service = TicketService(mock_repo)

    result = asyncio.run(service.get_ticket())

    assert len(result) == 1
    assert result[0] == mock_ticket
    mock_repo.get_all_tickets.assert_called_once_with(None, None)


def test_get_tickets_empty_list():
    mock_repo = Mock()
    mock_repo.get_all_tickets = AsyncMock(return_value=[])

    service = TicketService(mock_repo)

    result = asyncio.run(service.get_ticket())

    assert result == []
    mock_repo.get_all_tickets.assert_called_once_with(None, None)


def test_get_tickets_filter_by_priority():
    mock_repo = Mock()
    mock_ticket = Ticket(
        id=str(uuid4()),
        title="High Priority Ticket",
        description="Desc",
        priority="high",
        isOpen=True,
        email="user@example.com"
    )
    mock_repo.get_all_tickets = AsyncMock(return_value=[mock_ticket])

    service = TicketService(mock_repo)

    result = asyncio.run(service.get_ticket(priority="high"))

    assert len(result) == 1
    assert result[0].priority == "high"
    mock_repo.get_all_tickets.assert_called_once_with("high", None)


def test_get_tickets_filter_by_is_open():
    mock_repo = Mock()
    mock_ticket = Ticket(
        id=str(uuid4()),
        title="Open Ticket",
        description="Desc",
        priority="medium",
        isOpen=True,
        email="user@example.com"
    )
    mock_repo.get_all_tickets = AsyncMock(return_value=[mock_ticket])

    service = TicketService(mock_repo)

    result = asyncio.run(service.get_ticket(isOpen=True))

    assert len(result) == 1
    assert result[0].isOpen is True
    mock_repo.get_all_tickets.assert_called_once_with(None, True)


def test_get_tickets_filter_by_priority_and_is_open():
    mock_repo = Mock()
    mock_ticket = Ticket(
        id=str(uuid4()),
        title="Low Priority Closed",
        description="Desc",
        priority="low",
        isOpen=False,
        email="user@example.com"
    )
    mock_repo.get_all_tickets = AsyncMock(return_value=[mock_ticket])

    service = TicketService(mock_repo)

    result = asyncio.run(service.get_ticket(priority="low", isOpen=False))

    assert len(result) == 2
    assert result[0] == mock_ticket
    assert result[1] == mock_ticket
