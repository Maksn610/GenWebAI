import os
from app.utils import create_image_from_prompt
from PIL import Image


def test_create_image_from_prompt(tmp_path):
    prompt = "Test prompt for image"
    output_path = tmp_path / "test_image.png"

    create_image_from_prompt(prompt, str(output_path))

    assert os.path.exists(output_path)
    img = Image.open(output_path)
    assert img.size == (512, 256)


def test_create_image_from_prompt_fallback_font(tmp_path):
    output_path = os.path.join(tmp_path, "test.png")
    create_image_from_prompt("Test prompt for fallback font", output_path)
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0
