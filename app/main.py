from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.models import GenerateRequest
from app.generator import generate_website_content

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return JSONResponse(content={"status": "ok"})


@app.post("/generate")
async def generate_sites(request: GenerateRequest):
    page = generate_website_content(
        topic=request.topic,
        style=request.style,
        max_tokens=request.max_tokens
    )
    return page
