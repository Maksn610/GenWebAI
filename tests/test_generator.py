import pytest
import json
from unittest.mock import AsyncMock, patch
from app.generator import generate_website_content_async, select_sections


def test_select_sections():
    sections = select_sections()
    assert isinstance(sections, list)
    assert len(sections) == 5
    assert sections[0] == "Introduction"
    assert sections[-1] == "Summary"


@pytest.mark.asyncio
@patch("app.generator.RunnableWithMessageHistory.ainvoke", new_callable=AsyncMock)
async def test_generate_website_content_async(mock_ainvoke):
    mock_response = {
        "title": "Understanding Test Topic: A Beginner's Guide",
        "meta_description": "Test description",
        "sections": [
            {"heading": "Introduction", "text": "Intro text"},
            {"heading": "Summary", "text": "Summary text"}
        ]
    }

    class FakeAIMessage:
        def __init__(self, content):
            self.content = json.dumps(content)

    mock_ainvoke.return_value = FakeAIMessage(mock_response)

    result = await generate_website_content_async(topic="Test Topic", style="educational")

    assert "id" in result
    assert isinstance(result["title"], str)
    assert "Test Topic" in result["title"]
    assert "metrics" in result
    assert "token_count" in result["metrics"]
    assert "avg_section_similarity" in result["metrics"]
    assert "title_uniqueness_score" in result["metrics"]


@pytest.mark.asyncio
@patch("app.generator.RunnableWithMessageHistory.ainvoke", new_callable=AsyncMock)
async def test_generate_website_content_async_with_session(mock_ainvoke):
    mock_response = {
        "title": "Session Title",
        "meta_description": "Session description",
        "sections": [
            {"heading": "Introduction", "text": "Session intro"},
            {"heading": "Summary", "text": "Session summary"}
        ]
    }

    class FakeAIMessage:
        def __init__(self, content):
            self.content = json.dumps(content)

    mock_ainvoke.return_value = FakeAIMessage(mock_response)

    result = await generate_website_content_async(
        topic="Session Test",
        style="technical",
        session_id="test-session-123"
    )

    assert "id" in result
    assert "Session" in result["title"]
    assert "metrics" in result
    assert "token_count" in result["metrics"]
    assert "avg_section_similarity" in result["metrics"]
    assert "title_uniqueness_score" in result["metrics"]


@pytest.mark.asyncio
async def test_generate_with_variation_seed():
    result1 = await generate_website_content_async(
        topic="AI in Medicine",
        style="educational",
        variation_seed=123
    )
    result2 = await generate_website_content_async(
        topic="AI in Medicine",
        style="educational",
        variation_seed=123
    )

    assert isinstance(result1["title"], str)
    assert isinstance(result2["title"], str)
    assert result1["title"] != "" and result2["title"] != ""
