import pytest
from app.prompts import build_prompt, ALL_SECTIONS

def test_build_prompt_default_sections():
    topic = "Quantum Computing"
    style = "educational"

    prompt = build_prompt(topic, style)
    assert topic in prompt
    assert "Introduction" in prompt
    assert "Summary" in prompt
    sections_in_prompt = [section for section in ALL_SECTIONS if section in prompt]
    assert len(sections_in_prompt) >= 3

def test_build_prompt_custom_sections():
    topic = "AI"
    style = "marketing"
    custom_sections = ["Introduction", "Use Cases", "Summary"]

    prompt = build_prompt(topic, style, custom_sections)
    first_index = prompt.index(custom_sections[0])
    second_index = prompt.index(custom_sections[1])
    third_index = prompt.index(custom_sections[2])
    assert first_index < second_index < third_index

def test_build_prompt_tones():
    tones = {
        "educational": "clear and informative",
        "marketing": "persuasive and engaging",
        "technical": "precise and detailed",
        "unknown": "neutral"
    }
    topic = "Test Topic"

    for style, expected_tone in tones.items():
        prompt = build_prompt(topic, style)
        assert expected_tone in prompt

def test_few_shot_examples_in_prompt():
    topic = "Test"
    style = "educational"
    prompt = build_prompt(topic, style)

    if "Use Cases" in prompt:
        assert "In finance, quantum algorithms" in prompt
