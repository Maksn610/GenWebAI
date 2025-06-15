from pydantic import BaseModel, Field
from typing import Literal, Optional


class GenerateRequest(BaseModel):
    topic: str = Field(..., description="Main topic for the websites", examples=["Large Language Models"])
    pages_count: int = Field(..., ge=1, le=100, description="How many pages to generate", examples=[5])
    style: Literal["educational", "marketing", "technical"] = Field(
        ..., description="Tone or approach of the website", examples=["educational"]
    )
    max_tokens: int = Field(800, ge=100, le=2000, description="Maximum token limit for generation")
    temperature: Optional[float] = Field(0.9, ge=0.0, le=1.5, description="Controls randomness of generation")
    top_p: Optional[float] = Field(0.95, ge=0.0, le=1.0, description="Controls diversity of output")
    variation_seed: Optional[int] = Field(None, description="Seed for prompt variation randomness")
