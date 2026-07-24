import cProfile
import pstats
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import pytest

from app.models.ticket import Ticket


def test_profile_create_ticket_endpoint(client):
    profiler = cProfile.Profile()
    profiler.enable()

    payload = {
        "title": "Profiling Ticket Title",
        "description": "Profiling Ticket Description",
        "priority": "high",
        "email": "profiler@example.com",
        "isOpen": True
    }

    response = client.post("/tickets/", json=payload)

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("cumulative").print_stats(10)

    assert response.status_code == 200
    assert response.json()["status"] == 201


def test_profile_get_tickets_endpoint(client, mock_db_session):
    profiler = cProfile.Profile()
    profiler.enable()

    mock_ticket = Ticket(
        id=str(uuid4()),
        title="Profile Ticket",
        description="Profile Desc",
        priority="low",
        isOpen=True,
        email="profiler@example.com"
    )
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_ticket]
    mock_result.scalar_one_or_none.return_value = mock_ticket
    mock_db_session.execute = AsyncMock(return_value=mock_result)

    response = client.get("/tickets/get_tickets")

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("cumulative").print_stats(10)

    assert response.status_code == 200


def test_profile_update_ticket_endpoint(client, mock_db_session):
    profiler = cProfile.Profile()
    profiler.enable()

    ticket_id = str(uuid4())
    mock_ticket = Ticket(
        id=ticket_id,
        title="Original Title",
        description="Desc",
        priority="low",
        isOpen=True,
        email="profiler@example.com"
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_ticket
    mock_db_session.execute = AsyncMock(return_value=mock_result)

    response = client.put(f"/tickets/update?ticket_id={ticket_id}", json={"title": "Updated Title"})

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("cumulative").print_stats(10)

    assert response.status_code == 200


def test_profile_delete_ticket_endpoint(client, mock_db_session):
    profiler = cProfile.Profile()
    profiler.enable()

    ticket_id = str(uuid4())
    mock_ticket = Ticket(
        id=ticket_id,
        title="ToDelete",
        description="Desc",
        priority="low",
        isOpen=True,
        email="profiler@example.com"
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_ticket
    mock_db_session.execute = AsyncMock(return_value=mock_result)

    response = client.delete(f"/tickets/delete?ticket_id={ticket_id}")

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("cumulative").print_stats(10)

    assert response.status_code == 200


def test_profile_ai_summarize_endpoint(client):
    profiler = cProfile.Profile()
    profiler.enable()

    payload = {"ticket_description": "User cannot log in due to invalid credentials."}
    response = client.post("/ai/summarize", json=payload)

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("cumulative").print_stats(10)

    assert response.status_code == 200



