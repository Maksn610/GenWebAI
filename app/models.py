from pydantic import BaseModel, Field
from typing import Literal, Optional

class GenerateRequest(BaseModel):
    topic: str = Field(..., description="Main topic for the websites")
    pages_count: int = Field(..., ge=1, le=100, description="How many pages to generate")
    style: Literal["educational", "marketing", "technical"]
    max_tokens: int = Field(800, ge=100, le=2000)
    temperature: Optional[float] = Field(0.9, ge=0.0, le=1.5)
    top_p: Optional[float] = Field(0.95, ge=0.0, le=1.0)
    variation_seed: Optional[int] = Field(None, description="Seed for prompt variation randomness")
