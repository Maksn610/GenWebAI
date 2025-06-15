import pytest
import os
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.main.generate_website_content_async", new_callable=AsyncMock)
def test_generate_site(mock_generate):
    mock_generate.return_value = {
        "id": "test-id",
        "title": "Test Title",
        "meta_description": "Test description",
        "sections": [{"heading": "Intro", "text": "Some text"}],
        "file_path": "sites/test-id.html"
    }

    response = client.post("/generate", json={
        "topic": "Test Topic",
        "pages_count": 1,
        "style": "educational",
        "max_tokens": 800,
        "temperature": 0.9,
        "top_p": 0.95,
        "variation_seed": 42
    })

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test-id"
    assert "title" in data
    assert "sections" in data


def test_get_site_file():
    sites_dir = "sites"
    os.makedirs(sites_dir, exist_ok=True)
    file_path = os.path.join(sites_dir, "test-site.html")
    content = "<html><body>Test</body></html>"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        response = client.get("/site/test-site")
        assert response.status_code == 200
        assert content in response.text
    finally:
        os.remove(file_path)


def test_get_site_not_found():
    response = client.get("/site/non-existent-id")
    assert response.status_code == 404
    assert response.json() == {"error": "Site not found"}


@patch("aiofiles.open")
@pytest.mark.asyncio
async def test_get_logs(mock_aiofiles_open):
    mock_file = AsyncMock()
    mock_file.read.return_value = json.dumps([{"site_id": "123", "topic": "Test"}])
    mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

    response = client.get("/logs")
    assert response.status_code == 200
    assert response.json() == [{"site_id": "123", "topic": "Test"}]
