import pytest
from app.quality_metrics import (
    count_tokens,
    get_site_token_stats,
    get_section_similarities,
    get_title_uniqueness_score,
)


@pytest.fixture
def sections():
    return [
        {"text": "Quantum computing is powerful."},
        {"text": "It solves problems faster than classical computers."}
    ]


def test_count_tokens():
    text = "Hello world!"
    tokens = count_tokens(text)
    assert isinstance(tokens, int)
    assert tokens > 0


def test_get_site_token_stats(sections):
    tokens = get_site_token_stats(sections)
    assert isinstance(tokens, int)
    assert tokens > 0


def test_get_section_similarities(sections):
    score = get_section_similarities(sections)
    assert isinstance(score, float)
    assert 0 <= score <= 1


def test_get_title_uniqueness_score_no_prev():
    score = get_title_uniqueness_score("New Title", [])
    assert score == 1.0


def test_get_title_uniqueness_score_with_prev():
    previous = ["Old Title", "Another Page", "Quantum Insights"]
    score = get_title_uniqueness_score("Quantum Computing", previous)
    assert 0 <= score <= 1


def test_get_section_similarities_single_section():
    sections = [{"heading": "Intro", "text": "Only one section"}]
    similarity = get_section_similarities(sections)
    assert similarity == 0.0
