from dotenv import load_dotenv
from openai import OpenAI
import uuid
import os
import json
from typing import Dict
from jinja2 import Environment, FileSystemLoader
from app.prompts import build_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TEMPLATE_ENV = Environment(loader=FileSystemLoader("app/templates"))


def generate_website_content(topic: str, style: str, max_tokens: int = 800, temperature: float = 0.9,
                             top_p: float = 0.95) -> Dict:
    system_prompt = build_prompt(topic, style)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt}
        ],
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
    html_path = f"sites/site_{site_id}.html"

    template = TEMPLATE_ENV.get_template("site_template.html")
    rendered_html = template.render(
        title=result["title"],
        meta_description=result["meta_description"],
        sections=result["sections"]
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    return {
        "id": site_id,
        "title": result["title"],
        "meta_description": result["meta_description"],
        "sections": result["sections"],
        "file_path": html_path
    }
