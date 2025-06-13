import uuid
import os
import json
import datetime
from typing import Dict
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI
from dotenv import load_dotenv
import aiofiles
from app.prompts import build_prompt
from app.logger_config import logger

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY_DOCKER")
client = OpenAI(api_key=api_key)
TEMPLATE_ENV = Environment(loader=FileSystemLoader("app/templates"))


async def append_to_logs_async(entry: Dict):
    logs_path = "logs.json"
    try:
        async with aiofiles.open(logs_path, "r", encoding="utf-8") as f:
            content = await f.read()
            data = json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(entry)

    async with aiofiles.open(logs_path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, indent=2))


async def generate_website_content_async(topic: str, style: str, max_tokens: int = 800, temperature: float = 0.9,
                                         top_p: float = 0.95) -> Dict:
    logger.info(f"Calling OpenAI API with topic='{topic}', style='{style}'")
    system_prompt = build_prompt(topic, style)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system_prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p
    )

    content = response.choices[0].message.content
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Model did not return valid JSON.")

    site_id = str(uuid.uuid4())
    html_path = f"sites/{site_id}.html"

    template = TEMPLATE_ENV.get_template("site_template.html")
    rendered_html = template.render(
        title=result["title"],
        meta_description=result["meta_description"],
        sections=result["sections"]
    )

    logger.info(f"Saving HTML to: {html_path}")
    async with aiofiles.open(html_path, "w", encoding="utf-8") as f:
        await f.write(rendered_html)

    log_entry = {
        "site_id": site_id,
        "topic": topic,
        "style": style,
        "file_path": html_path,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

    logger.info(f"Logging entry to logs.json for site_id: {site_id}")
    await append_to_logs_async(log_entry)

    return {
        "id": site_id,
        "title": result["title"],
        "meta_description": result["meta_description"],
        "sections": result["sections"],
        "file_path": html_path
    }


def generate_website_content(*args, **kwargs):
    import asyncio
    return asyncio.run(generate_website_content_async(*args, **kwargs))
