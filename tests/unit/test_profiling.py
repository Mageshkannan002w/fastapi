import cProfile
import pstats
import asyncio
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from app.services.ticket_service import TicketService
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdateData


def test_cprofile_get_ticket_service():
    profiler = cProfile.Profile()
    profiler.enable()

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

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("cumulative").print_stats(10)

    assert result == mock_ticket


def test_cprofile_create_ticket_service():
    profiler = cProfile.Profile()
    profiler.enable()

    mock_repo = AsyncMock()
    mock_repo.create_ticket.side_effect = lambda ticket: ticket
    service = TicketService(mock_repo)

    ticket_data = TicketCreate(
        title="Profile Ticket",
        description="Profile Desc",
        priority="medium",
        isOpen=True,
        email="profile@example.com"
    )

    result = asyncio.run(service.create_ticket(ticket_data))

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("cumulative").print_stats(10)

    assert result.title == "Profile Ticket"


def test_cprofile_update_ticket_service():
    profiler = cProfile.Profile()
    profiler.enable()

    mock_repo = AsyncMock()
    ticket_id = uuid4()
    mock_ticket = Ticket(
        id=str(ticket_id),
        title="Original Title",
        description="Desc",
        priority="low",
        isOpen=True,
        email="profile@example.com"
    )
    mock_repo.get_ticket_by_id.return_value = mock_ticket
    mock_repo.update_ticket.return_value = mock_ticket
    service = TicketService(mock_repo)

    update_data = TicketUpdateData(title="New Profile Title")
    result = asyncio.run(service.update_ticket(ticket_id, update_data))

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("cumulative").print_stats(10)

    assert result == mock_ticket
