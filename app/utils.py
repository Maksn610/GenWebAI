import os
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap


def create_image_from_prompt(prompt: str, output_path: str, width: int = 512, height: int = 256,
                             font_size: int = 16) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Wrap text to fit image width
    max_chars_per_line = int(width / (font_size * 0.6))
    wrapped_text = "\n".join(wrap(prompt, width=max_chars_per_line))

    draw.text((10, 10), wrapped_text, fill=(0, 0, 0), font=font)
    image.save(output_path)
