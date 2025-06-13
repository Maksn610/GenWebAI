import pytest
import json
from unittest.mock import patch
from app.generator import select_sections, generate_website_content_async

@pytest.mark.asyncio
async def test_select_sections():
    sections = select_sections()
    assert isinstance(sections, list)
    assert 3 <= len(sections) <= 5
    assert sections[0] == "Introduction"
    assert sections[-1] == "Summary"
    assert len(set(sections)) == len(sections)

class FakeAIMessage:
    def __init__(self, content):
        self.content = content

@pytest.mark.asyncio
@patch("app.generator.RunnableSequence.invoke")
async def test_generate_website_content_async(mock_invoke):
    mock_response = {
        "title": "Test Title",
        "meta_description": "Test description",
        "sections": [
            {"heading": "Introduction", "text": "Intro text"},
            {"heading": "Summary", "text": "Summary text"}
        ]
    }
    mock_invoke.return_value = FakeAIMessage(json.dumps(mock_response))

    topic = "Test Topic"
    style = "educational"

    result = await generate_website_content_async(topic, style)

    assert "id" in result
    assert result["title"] == mock_response["title"]
    assert result["meta_description"] == mock_response["meta_description"]
    assert isinstance(result["sections"], list)
    assert result["file_path"].endswith(".html")

@pytest.mark.asyncio
@patch("app.generator.RunnableSequence.invoke")
async def test_generate_website_content_async_with_seed(mock_invoke):
    mock_response = {
        "title": "Seeded Title",
        "meta_description": "Seeded description",
        "sections": [
            {"heading": "Introduction", "text": "Seeded intro"},
            {"heading": "Summary", "text": "Seeded summary"}
        ]
    }
    mock_invoke.return_value = FakeAIMessage(json.dumps(mock_response))

    topic = "Seed Test"
    style = "educational"
    seed = 42

    result1 = await generate_website_content_async(topic, style, variation_seed=seed)
    result2 = await generate_website_content_async(topic, style, variation_seed=seed)

    assert result1["title"] == result2["title"]
    assert result1["sections"] == result2["sections"]
