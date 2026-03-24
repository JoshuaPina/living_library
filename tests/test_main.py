import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock

# Set environment variable BEFORE importing main
os.environ["DATABASE_URL"] = "postgresql+asyncpg://test:test@localhost:5432/testdb"

from fastapi.testclient import TestClient
from main import app

# We mock sentence transformers to avoid downloading models and loading them in tests
@pytest.fixture(autouse=True)
def mock_sentence_transformer():
    with patch("main.SentenceTransformer") as mock:
        mock_instance = MagicMock()
        # Mock encode returning something that has .tolist()
        mock_array = MagicMock()
        mock_array.tolist.return_value = [0.1, 0.2, 0.3]
        mock_instance.encode.return_value = mock_array
        mock.return_value = mock_instance
        yield mock

@pytest.fixture
def client():
    # TestClient inside a context manager calls startup and shutdown events
    with TestClient(app) as c:
        yield c

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

@pytest.fixture
def mock_db_session():
    with patch("main.async_session") as mock_session_maker:
        mock_session = AsyncMock()
        mock_session_maker.return_value.__aenter__.return_value = mock_session
        yield mock_session

def test_health_check_healthy(client, mock_db_session):
    mock_db_session.execute.return_value = MagicMock()

    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "connected"}

def test_health_check_unhealthy(client, mock_db_session):
    mock_db_session.execute.side_effect = Exception("DB Connection Failed")

    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "unhealthy", "error": "Internal server error"}

def test_get_stats_success(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (10, 5, 3, 100, 100, {"1": 5, "2": 3, "3": 2})
    mock_db_session.execute.return_value = mock_result

    response = client.get("/api/stats")
    assert response.status_code == 200
    assert response.json() == {
        "total_materials": 10,
        "total_authors": 5,
        "total_topics": 3,
        "total_chunks": 100,
        "total_embeddings": 100,
        "materials_by_tier": {"1": 5, "2": 3, "3": 2}
    }

def test_get_stats_no_data(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = None
    mock_db_session.execute.return_value = mock_result

    response = client.get("/api/stats")
    assert response.status_code == 200
    assert response.json() == {"error": "No stats available"}

def test_get_stats_exception(client, mock_db_session):
    mock_db_session.execute.side_effect = Exception("DB Error")

    response = client.get("/api/stats")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}

def test_browse_library_success(client, mock_db_session):
    mock_result = MagicMock()
    # Returns (material_id, title, subtitle, edition, year, type, tier, status, topics, authors, pages, is_accessible, storage_provider)
    mock_result.fetchall.return_value = [
        (1, "Test Book", "Subtitle", "1st", 2023, "Book", 1, "processed", "Science", "John Doe", 100, True, "local")
    ]
    mock_db_session.execute.return_value = mock_result

    response = client.get("/api/library/browse?topic=Science")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["materials"][0]["title"] == "Test Book"
    assert data["materials"][0]["topics"] == "Science"

def test_browse_library_exception(client, mock_db_session):
    mock_db_session.execute.side_effect = Exception("Browse error")

    response = client.get("/api/library/browse")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}

def test_get_topics_success(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.fetchall.return_value = [("Math",), ("Science",)]
    mock_db_session.execute.return_value = mock_result

    response = client.get("/api/library/topics")
    assert response.status_code == 200
    assert response.json() == {"topics": ["Math", "Science"]}

def test_get_topics_exception(client, mock_db_session):
    mock_db_session.execute.side_effect = Exception("Topic error")

    response = client.get("/api/library/topics")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}


@patch("asyncpg.connect", new_callable=AsyncMock)
def test_semantic_search_success(mock_connect, client):
    # Mock connection and fetch results
    mock_conn = AsyncMock()
    mock_connect.return_value = mock_conn
    mock_conn.fetch.return_value = [
        {
            "chunk_id": 1,
            "material_id": 2,
            "title": "Search Result Book",
            "page_number": 5,
            "chunk_text": "This is a relevant chunk.",
            "similarity": 0.95
        }
    ]

    response = client.post("/api/search/semantic", json={"query": "test query", "topic": "Math"})

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "test query"
    assert len(data["results"]) == 1
    assert data["results"][0]["title"] == "Search Result Book"
    assert data["results"][0]["similarity"] == 0.95

    # Verify close was called
    mock_conn.close.assert_called_once()

@patch("asyncpg.connect", new_callable=AsyncMock)
def test_semantic_search_exception(mock_connect, client):
    mock_connect.side_effect = Exception("Search DB error")

    response = client.post("/api/search/semantic", json={"query": "test query"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}

def test_get_material_info_success_supabase(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = ("Cloud Book", "path.pdf", "supabase", "bucket", True)
    mock_db_session.execute.return_value = mock_result

    with patch("main.supabase_client") as mock_supabase:
        mock_supabase.storage.from_().get_public_url.return_value = "http://example.com/path.pdf"

        response = client.get("/api/material/1/info")

        assert response.status_code == 200
        assert response.json() == {
            "title": "Cloud Book",
            "type": "supabase",
            "url": "http://example.com/path.pdf"
        }

def test_get_material_info_success_local(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = ("Local Book", "path.pdf", "local", None, True)
    mock_db_session.execute.return_value = mock_result

    response = client.get("/api/material/1/info")

    assert response.status_code == 200
    assert response.json() == {
        "title": "Local Book",
        "type": "local"
    }

def test_get_material_info_not_found(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = None
    mock_db_session.execute.return_value = mock_result

    response = client.get("/api/material/1/info")

    assert response.status_code == 404
    assert response.json() == {"detail": "Material not found"}

def test_get_material_info_not_accessible(client, mock_db_session):
    mock_result = MagicMock()
    # is_accessible is False
    mock_result.fetchone.return_value = ("Forbidden Book", "path.pdf", "local", None, False)
    mock_db_session.execute.return_value = mock_result

    response = client.get("/api/material/1/info")

    assert response.status_code == 403
    assert response.json() == {"detail": "File not accessible"}

def test_get_duplicates_success(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.fetchall.return_value = [
        (1, "Book A", "Book B", 0.98, "title_similarity", "pending")
    ]
    mock_db_session.execute.return_value = mock_result

    response = client.get("/api/duplicates")

    assert response.status_code == 200
    assert response.json() == {
        "duplicates": [
            {
                "candidate_id": 1,
                "title_1": "Book A",
                "title_2": "Book B",
                "similarity_score": 0.98,
                "detection_method": "title_similarity",
                "status": "pending"
            }
        ]
    }

def test_get_duplicates_exception(client, mock_db_session):
    mock_db_session.execute.side_effect = Exception("Duplicates error")

    response = client.get("/api/duplicates")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}


@patch("main.fitz.open")
def test_get_pdf_page_local_success(mock_fitz_open, client, mock_db_session, tmp_path):
    mock_result = MagicMock()
    # (storage_path, storage_provider, storage_bucket, is_accessible)
    mock_result.fetchone.return_value = ("test.pdf", "local", None, True)
    mock_db_session.execute.return_value = mock_result

    mock_doc = MagicMock()
    mock_page = MagicMock()
    mock_pix = MagicMock()
    mock_pix.tobytes.return_value = b"image_data"
    mock_page.get_pixmap.return_value = mock_pix

    mock_doc.__len__.return_value = 5  # Length of doc is 5 pages
    mock_doc.__getitem__.return_value = mock_page
    mock_fitz_open.return_value = mock_doc

    with patch("main.PDF_BASE_DIR", tmp_path):
        # Create a dummy file so exists() returns True
        dummy_file = tmp_path / "test.pdf"
        dummy_file.touch()

        response = client.get("/api/pdf/1/page/2")

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert response.content == b"image_data"

@patch("main.fitz.open")
def test_get_pdf_page_local_not_found_on_disk(mock_fitz_open, client, mock_db_session, tmp_path):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = ("missing.pdf", "local", None, True)
    mock_db_session.execute.return_value = mock_result

    with patch("main.PDF_BASE_DIR", tmp_path):
        # We don't create the file, so exists() is False
        response = client.get("/api/pdf/1/page/2")

        assert response.status_code == 404
        assert response.json() == {"detail": "PDF file not found on disk"}

@patch("main.fitz.open")
def test_get_pdf_page_supabase_success(mock_fitz_open, client, mock_db_session):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = ("test.pdf", "supabase", "bucket", True)
    mock_db_session.execute.return_value = mock_result

    mock_doc = MagicMock()
    mock_page = MagicMock()
    mock_pix = MagicMock()
    mock_pix.tobytes.return_value = b"image_data"
    mock_page.get_pixmap.return_value = mock_pix

    mock_doc.__len__.return_value = 5
    mock_doc.__getitem__.return_value = mock_page
    mock_fitz_open.return_value = mock_doc

    with patch("main.supabase_client") as mock_supabase:
        mock_supabase.storage.from_().download.return_value = b"pdf_data"

        response = client.get("/api/pdf/1/page/1")

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert response.content == b"image_data"

def test_get_pdf_page_db_metadata_missing(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = None
    mock_db_session.execute.return_value = mock_result

    response = client.get("/api/pdf/1/page/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "File metadata not found in database"}

def test_get_pdf_page_not_accessible(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = ("test.pdf", "local", None, False)
    mock_db_session.execute.return_value = mock_result

    response = client.get("/api/pdf/1/page/1")

    assert response.status_code == 403
    assert response.json() == {"detail": "File not accessible"}


@patch("main.fitz.open")
def test_get_pdf_page_out_of_bounds(mock_fitz_open, client, mock_db_session, tmp_path):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = ("test.pdf", "local", None, True)
    mock_db_session.execute.return_value = mock_result

    mock_doc = MagicMock()
    mock_doc.__len__.return_value = 5  # Only 5 pages
    mock_fitz_open.return_value = mock_doc

    with patch("main.PDF_BASE_DIR", tmp_path):
        dummy_file = tmp_path / "test.pdf"
        dummy_file.touch()

        response = client.get("/api/pdf/1/page/6")

        assert response.status_code == 404
        assert response.json() == {"detail": "Page not found in document"}
        assert mock_doc.close.called
