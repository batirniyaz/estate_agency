from pydantic import BaseModel, Field
import datetime
from typing import List, Optional


class LandBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=36, description="The title of the land", examples=["First land"])
