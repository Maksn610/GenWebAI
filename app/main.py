from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from app.models import GenerateRequest
from app.generator import generate_website_content_async
import aiofiles
import os
import json
from app.logger_config import logger

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    return JSONResponse(content={"status": "ok"})

@app.post("/generate")
async def generate_sites(request: GenerateRequest):
    logger.info(f"Received request to generate site: topic='{request.topic}', style='{request.style}'")
    try:
        page = await generate_website_content_async(
            topic=request.topic,
            style=request.style,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            variation_seed=request.variation_seed if hasattr(request, "variation_seed") else None,
        )
        logger.info(f"Successfully generated site: {page['id']}")
        return page
    except Exception as e:
        logger.exception("Error during site generation")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/site/{site_id}")
async def get_site(site_id: str):
    file_path = f"sites/{site_id}.html"
    if not os.path.exists(file_path):
        logger.warning(f"Site not found: {site_id}")
        return {"error": "Site not found"}
    logger.info(f"Returning site: {site_id}")
    return FileResponse(file_path, media_type="text/html")

@app.get("/logs")
async def get_logs():
    try:
        async with aiofiles.open("logs.json", "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
