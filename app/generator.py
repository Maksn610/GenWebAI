import uuid
import os
import json
import datetime
import random
from typing import Dict
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import aiofiles
from app.prompts import build_prompt, ALL_SECTIONS
from app.logger_config import logger
from app.utils import create_image_from_prompt
from app.quality_metrics import (
    get_site_token_stats,
    get_section_similarities,
    get_title_uniqueness_score,
)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.schema.runnable import RunnableSequence
from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from app.memory import memory_manager

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY_DOCKER")

TEMPLATE_ENV = Environment(loader=FileSystemLoader("app/templates"))

llm = ChatOpenAI(model_name="gpt-4", temperature=0.9, max_tokens=800)

# Tools
duckduckgo_tool = DuckDuckGoSearchRun()
wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tools = [
    Tool(name="duckduckgo_search", func=duckduckgo_tool.run, description="Search the web using DuckDuckGo"),
    Tool(name="wikipedia", func=wikipedia_tool.run, description="Get factual info from Wikipedia")
]

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


def select_sections():
    intro = "Introduction"
    summary = "Summary"
    middle = random.sample([s for s in ALL_SECTIONS if s not in (intro, summary)], k=3)
    sections = [intro] + middle + [summary]
    logger.info(f"Selected sections: {sections}")
    return sections


async def generate_website_content_async(
    topic: str,
    style: str,
    max_tokens: int = 800,
    temperature: float = 0.9,
    top_p: float = 0.95,
    variation_seed: int | None = None,
    session_id: str | None = None,
) -> dict:
    sections = random.sample(ALL_SECTIONS, random.randint(3, 5))
    prompt_text = build_prompt(topic, style, sections)

    llm = ChatOpenAI(model_name="gpt-4", temperature=temperature, max_tokens=max_tokens)
    prompt = PromptTemplate(template=prompt_text, input_variables=["input"])
    base_runnable = RunnableSequence(prompt, llm).with_config({"tags": ["site_generation"]})

    if session_id:
        runnable = RunnableWithMessageHistory(
            base_runnable,
            get_session_history=memory_manager.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
            tools=tools,
        )
        response = await runnable.ainvoke(
            {"input": topic},
            config={"configurable": {"session_id": session_id}},
        )
    else:
        response = await base_runnable.ainvoke({"input": topic})

    content_str = response.content if hasattr(response, "content") else str(response)
    result = json.loads(content_str)

    site_id = str(uuid.uuid4())
    html_path = f"sites/{site_id}.html"
    os.makedirs("sites", exist_ok=True)
    os.makedirs("sites/images", exist_ok=True)

    for i, section in enumerate(result["sections"]):
        prompt = section.get("image_prompt")
        if prompt:
            image_filename = f"{site_id}_{i}.png"
            image_path = f"sites/images/{image_filename}"
            create_image_from_prompt(prompt, image_path)
            section["image_path"] = f"images/{image_filename}"

    token_count = get_site_token_stats(result["sections"])
    avg_similarity = round(get_section_similarities(result["sections"]), 4)

    try:
        async with aiofiles.open("logs.json", "r", encoding="utf-8") as f:
            past_content = await f.read()
            past_logs = json.loads(past_content) if past_content else []
            past_titles = [entry.get("title", "") for entry in past_logs if "title" in entry]
    except Exception:
        past_titles = []

    title_uniqueness = get_title_uniqueness_score(result["title"], past_titles)

    result["metrics"] = {
        "token_count": token_count,
        "avg_section_similarity": avg_similarity,
        "title_uniqueness_score": title_uniqueness,
    }

    template = TEMPLATE_ENV.get_template("site_template.html")
    rendered_html = template.render(
        title=result["title"],
        meta_description=result["meta_description"],
        sections=result["sections"],
    )

    async with aiofiles.open(html_path, "w", encoding="utf-8") as f:
        await f.write(rendered_html)

    entry = {
        "site_id": site_id,
        "topic": topic,
        "style": style,
        "file_path": html_path,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "title": result["title"],
        "metrics": result["metrics"],
    }

    try:
        async with aiofiles.open("logs.json", "r+", encoding="utf-8") as f:
            content = await f.read()
            logs = json.loads(content) if content else []
            logs.append(entry)
            await f.seek(0)
            await f.write(json.dumps(logs, ensure_ascii=False, indent=2))
            await f.truncate()
    except FileNotFoundError:
        async with aiofiles.open("logs.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps([entry], ensure_ascii=False, indent=2))

    return {
        "id": site_id,
        "title": result["title"],
        "meta_description": result["meta_description"],
        "sections": result["sections"],
        "file_path": html_path,
        "metrics": result["metrics"],
    }



def generate_website_content(*args, **kwargs):
    import asyncio
    return asyncio.run(generate_website_content_async(*args, **kwargs))
