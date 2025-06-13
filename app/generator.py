from openai import OpenAI
import uuid
import os
import json
from typing import Dict
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_website_content(topic: str, style: str, max_tokens: int = 800) -> Dict:
    system_prompt = f"""
You are an expert content writer. Generate a complete plan and content for a single-page HTML website about the topic: '{topic}'.
The writing style should be '{style}'.
Include:
- A unique, creative page title
- A short SEO-friendly meta description
- 3 to 5 well-structured sections with headings and paragraphs
Return in JSON format with fields: title, meta_description, sections (each with heading and text).
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.9,
        top_p=0.95
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
