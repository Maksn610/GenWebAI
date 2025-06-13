from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    return JSONResponse(content={"status": "ok"})
