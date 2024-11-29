from pydantic import BaseModel, Field
from typing import Optional
import datetime


class DistrictBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="The name of the district", examples=["Sergeli"])


class DistrictCreate(DistrictBase):
    pass


class DistrictUpdate(DistrictBase):
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="The name of the district", examples=["Sergeli"])


class DistrictResponse(DistrictBase):
    id: int = Field(..., description="The ID of the district")
    created_at: datetime.datetime = Field(..., description="The time the district was created")
    updated_at: datetime.datetime = Field(..., description="The time the district was updated")

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
