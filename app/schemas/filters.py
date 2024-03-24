from pydantic import BaseModel, Field
from typing import Optional


class FilteringParams(BaseModel):
    sort_order: str = Field(default="ASC", description="Sort order: ASC or DESC")
    page_size: int = Field(default=10, ge=1, description="Number of tasks per page")
    page: int = Field(default=1, ge=1, description="Page number")
