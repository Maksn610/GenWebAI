from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from app.models import GenerateRequest
from app.generator import generate_website_content_async
import aiofiles
import os
import json

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    return JSONResponse(content={"status": "ok"})

@app.post("/generate")
async def generate_sites(request: GenerateRequest):
    page = await generate_website_content_async(
        topic=request.topic,
        style=request.style,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p
    )
    return page

@app.get("/site/{site_id}")
async def get_site(site_id: str):
    file_path = f"sites/{site_id}.html"
    if not os.path.exists(file_path):
        return {"error": "Site not found"}
    return FileResponse(file_path, media_type="text/html")

@app.get("/logs")
async def get_logs():
    try:
        async with aiofiles.open("logs.json", "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
