import os
import json
import aiofiles
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
from typing import List, Dict


def create_image_from_prompt(prompt: str, output_path: str, width: int = 512, height: int = 256,
                             font_size: int = 16) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    max_chars_per_line = int(width / (font_size * 0.6))
    wrapped_text = "\n".join(wrap(prompt, width=max_chars_per_line))

    draw.text((10, 10), wrapped_text, fill=(0, 0, 0), font=font)
    image.save(output_path)


async def read_logs_file(path: str = "logs.json") -> List[Dict]:
    try:
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
