from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.models import GenerateRequest
import uuid

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    return JSONResponse(content={"status": "ok"})

@app.post("/generate")
async def generate_sites(request: GenerateRequest):
    job_id = str(uuid.uuid4())
    return {
        "message": f"Generation started",
        "topic": request.topic,
        "count": request.pages_count,
        "style": request.style,
        "max_tokens": request.max_tokens,
        "job_id": job_id
    }
