from pydantic import BaseModel, Field
from typing import Literal

class GenerateRequest(BaseModel):
    topic: str = Field(..., description="Main topic for the websites")
    pages_count: int = Field(..., ge=1, le=100, description="How many pages to generate")
    style: Literal["educational", "marketing", "technical"] = Field(..., description="Content style")
    max_tokens: int = Field(800, ge=100, le=2000, description="Maximum tokens per site")
