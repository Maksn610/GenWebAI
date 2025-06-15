from PIL import Image, ImageDraw, ImageFont
import os


def create_image_from_prompt(prompt: str, output_path: str, width=512, height=256):
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    draw.text((10, 10), prompt, fill=(0, 0, 0), font=font)
    image.save(output_path)
