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


@pytest.mark.parametrize("invalid_id,expected_error", [
    (None, "Ticket ID is required"),
])
def test_delete_ticket_invalid_id(invalid_id, expected_error):
    mock_repo = Mock()
    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.delete_ticket(invalid_id))

    assert str(exc_info.value) == expected_error
    mock_repo.get_ticket_by_id.assert_not_called()
    mock_repo.delete_ticket.assert_not_called()


@pytest.mark.parametrize("get_by_id_result,delete_result,expected_error", [
    (None, True, "Ticket not found"),
    (Ticket(id=str(uuid4()), title="D", description="D", priority="low", isOpen=True, email="a@b.com"), False, "An Error Occurred"),
])
def test_delete_ticket_error_scenarios(get_by_id_result, delete_result, expected_error):
    mock_repo = Mock()
    ticket_id = uuid4()

    mock_repo.get_ticket_by_id = AsyncMock(return_value=get_by_id_result)
    mock_repo.delete_ticket = AsyncMock(return_value=delete_result)

    service = TicketService(mock_repo)

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(service.delete_ticket(ticket_id))

    assert str(exc_info.value) == expected_error
    mock_repo.get_ticket_by_id.assert_called_once_with(ticket_id, None, None)
    if get_by_id_result is not None:
        mock_repo.delete_ticket.assert_called_once_with(ticket_id)
    else:
        mock_repo.delete_ticket.assert_not_called()
