import uuid
import os
import json
import datetime
import random
from dotenv import load_dotenv
import aiofiles
from app.prompts import build_prompt, ALL_SECTIONS
from app.logger_config import logger
from app.utils import create_image_from_prompt, read_logs_file
from app.quality_metrics import (
    get_site_token_stats,
    get_section_similarities,
    get_title_uniqueness_score,
)
from app.memory import memory_manager
from app.config import TEMPLATE_ENV
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.schema.runnable import RunnableSequence
from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

load_dotenv()

duckduckgo_tool = DuckDuckGoSearchRun()
wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tools = [
    Tool(name="duckduckgo_search", func=duckduckgo_tool.run, description="Search the web using DuckDuckGo"),
    Tool(name="wikipedia", func=wikipedia_tool.run, description="Get factual info from Wikipedia"),
]


def select_sections() -> list[str]:
    intro = "Introduction"
    summary = "Summary"
    middle = random.sample([s for s in ALL_SECTIONS if s not in (intro, summary)], k=3)
    sections = [intro] + middle + [summary]
    logger.info(f"Selected sections: {sections}")
    return sections


def build_runnable(prompt_text: str, temperature: float, max_tokens: int, top_p: float, session_id: str | None = None):
    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
    )
    prompt = PromptTemplate(template=prompt_text, input_variables=["input"])
    base_runnable = RunnableSequence(prompt, llm).with_config({"tags": ["site_generation"]})

    if session_id:
        return (
            RunnableWithMessageHistory(
                base_runnable,
                get_session_history=memory_manager.get_session_history,
                input_messages_key="input",
                history_messages_key="history",
                tools=tools,
            ),
            {"input": prompt_text},
            {"configurable": {"session_id": session_id}},
        )
    return base_runnable, {"input": prompt_text}, None


async def run_generation(runnable, input_data: dict, config: dict | None):
    if config:
        response = await runnable.ainvoke(input_data, config=config)
    else:
        response = await runnable.ainvoke(input_data)
    return response.content if hasattr(response, "content") else str(response)


def render_images(result: dict, site_id: str):
    os.makedirs("sites/images", exist_ok=True)
    for i, section in enumerate(result["sections"]):
        prompt = section.get("image_prompt")
        if prompt:
            image_filename = f"{site_id}_{i}.png"
            image_path = f"sites/images/{image_filename}"
            create_image_from_prompt(prompt, image_path)
            section["image_path"] = f"images/{image_filename}"


def calculate_quality_metrics(result: dict, past_titles: list[str]) -> dict:
    token_count = get_site_token_stats(result["sections"])
    avg_similarity = round(get_section_similarities(result["sections"]), 4)
    title_uniqueness = get_title_uniqueness_score(result["title"], past_titles)
    return {
        "token_count": token_count,
        "avg_section_similarity": avg_similarity,
        "title_uniqueness_score": title_uniqueness,
    }


async def render_html_to_file(result: dict, site_id: str) -> str:
    os.makedirs("sites", exist_ok=True)
    html_path = f"sites/{site_id}.html"
    template = TEMPLATE_ENV.get_template("site_template.html")
    rendered_html = template.render(
        title=result["title"],
        meta_description=result["meta_description"],
        sections=result["sections"],
    )
    async with aiofiles.open(html_path, "w", encoding="utf-8") as f:
        await f.write(rendered_html)
    return html_path


async def log_generation(entry: dict):
    logs = await read_logs_file("logs.json")
    logs.append(entry)
    async with aiofiles.open("logs.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps(logs, indent=2, ensure_ascii=False))


async def generate_website_content_async(
        topic: str,
        style: str,
        max_tokens: int = 800,
        temperature: float = 0.9,
        top_p: float = 0.95,
        variation_seed: int | None = None,
        session_id: str | None = None,
) -> dict:
    if variation_seed is not None:
        random.seed(variation_seed)

    logger.info(f"Generating website for topic='{topic}', style='{style}'")
    sections = select_sections()
    prompt_text = build_prompt(topic, style, sections)
    runnable, input_data, config = build_runnable(prompt_text, temperature, max_tokens, top_p, session_id)
    logger.info("Calling LangChain runnable...")
    response_str = await run_generation(runnable, input_data, config)

    try:
        result = json.loads(response_str)
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON response from LLM")
        raise

    site_id = str(uuid.uuid4())
    render_images(result, site_id)

    past_logs = await read_logs_file("logs.json")
    past_titles = [entry.get("title", "") for entry in past_logs if "title" in entry]

    result["metrics"] = calculate_quality_metrics(result, past_titles)
    html_path = await render_html_to_file(result, site_id)

    entry = {
        "site_id": site_id,
        "topic": topic,
        "style": style,
        "file_path": html_path,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "title": result["title"],
        "metrics": result["metrics"],
    }
    await log_generation(entry)

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
