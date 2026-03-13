import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch

# Need to set env variables before importing main to avoid errors
import os
os.environ["DATABASE_URL"] = "postgresql://fakeuser:fakepassword@localhost:5432/fakedb"

from main import app

client = TestClient(app)

def test_get_topics_success():
    """Test successful retrieval of topics."""
    class MockSessionContext:
        async def __aenter__(self):
            mock_session = MagicMock()
            mock_result = MagicMock()
            mock_result.fetchall.return_value = [("Biology",), ("Chemistry",), ("Physics",)]
            mock_session.execute = AsyncMock(return_value=mock_result)
            return mock_session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch('main.async_session', return_value=MockSessionContext()):
        response = client.get("/api/library/topics")

    assert response.status_code == 200
    assert response.json() == {"topics": ["Biology", "Chemistry", "Physics"]}

def test_get_topics_database_error():
    """Test handling of database errors when retrieving topics."""
    class MockSessionContext:
        async def __aenter__(self):
            mock_session = MagicMock()
            mock_session.execute = AsyncMock(side_effect=Exception("Database connection failed"))
            return mock_session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch('main.async_session', return_value=MockSessionContext()):
        response = client.get("/api/library/topics")

    assert response.status_code == 500
    assert response.json() == {"detail": "Database connection failed"}
