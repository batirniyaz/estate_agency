import datetime
from pydantic import BaseModel, Field
from typing import Optional


class MetroBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="The name of the metro", examples=["Sergeli"])


class MetroCreate(MetroBase):
    pass


class MetroUpdate(MetroBase):
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="The name of the metro", examples=["Sergeli"])


class MetroResponse(MetroBase):
    id: int = Field(..., description="The ID of the metro")
    created_at: datetime.datetime = Field(..., description="The time the metro was created")
    updated_at: datetime.datetime = Field(..., description="The time the metro was updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Sergeli",
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }

