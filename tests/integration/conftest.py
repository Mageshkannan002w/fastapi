import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.core.database import get_db
from app.services.aws_bedrock_service import FakeBedrockService
from app.api.ai import get_bedrock_service


@pytest.fixture
def mock_db_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def client(mock_db_session):
    async def _override_get_db():
        yield mock_db_session

    def _override_get_bedrock_service():
        return FakeBedrockService()

    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_bedrock_service] = _override_get_bedrock_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
