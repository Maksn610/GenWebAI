from dotenv import load_dotenv
from openai import OpenAI
import uuid
import os
import json
from typing import Dict
from app.prompts import build_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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

    return {
        "id": str(uuid.uuid4()),
        "title": result["title"],
        "meta_description": result["meta_description"],
        "sections": result["sections"]
    }
