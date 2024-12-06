from pydantic import BaseModel, Field
import datetime
from typing import List, Optional

from app.object.models import Category, ActionType, LocationLand, HouseCondition, CurrentStatus


class LandMediaResponse(BaseModel):
    id: int = Field(..., description="The ID of the image", examples=[1])
    url: str = Field(..., description="The URL of the image", examples=["http://example.com/image.jpg"])
    media_type: str = Field(..., description="The type of the media", examples=["image"])
    land_id: int = Field(..., description="The ID of the land", examples=[1])
    created_at: datetime.datetime = Field(..., description="The time the image was created",
                                          examples=["2021-08-01T12:00:00"])
    updated_at: datetime.datetime = Field(..., description="The time the image was updated",
                                          examples=["2021-08-01T12:00:00"])

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "url": "http://example.com/image.jpg",
                "media_type": "image",
                "land_id": 1,
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }


class LandBase(BaseModel):
    district: str = Field(..., description="The district name of the land",
                          examples=["Yunusabad"])
    title: str = Field(..., min_length=3, max_length=50, description="The title of the land",
                       examples=["Land for sale"])
    category: Category = Field(..., description="The category of the land",
                               examples=["LAND", "APARTMENT", "COMMERCIAL"])
    action_type: ActionType = Field(..., description="The action type of the land",
                                    examples=["SALE", "RENT"])
    description: Optional[str] = Field(None, max_length=6000, description="The description of the land", examples=["Land for sale"])
    comment: Optional[str] = Field(None, max_length=6000, description="The comment of the land", examples=["Land for sale"])
    price: int = Field(..., description="The price of the land", examples=[100000])
    rooms: int = Field(..., description="The number of rooms in the land", examples=[1, 2, 3, 4, 5, 6])
    square_area: int = Field(..., description="The square area of the land", examples=[100])
    floor_number: int = Field(..., description="The floor number of the land", examples=[23])
    location: LocationLand = Field(..., description="The location of the land", examples=["CITY", "SUBURB"])
    furnished: bool = Field(True, description="The furnished status of the land", examples=[True, False])
    house_condition: HouseCondition = Field(..., description="The house condition of the land",
                                            examples=["EURO", "NORMAL", "REPAIR"])
    current_status: CurrentStatus = Field(None, description='The current status of the apartment',
                                          examples=['FREE', 'BUSY', 'SOON'])
    parking_place: bool = Field(..., description="The parking place status of the land", examples=[True, False])
    agent_percent: Optional[int] = Field(..., description="The agent percent of the land", examples=[10])
    agent_commission: Optional[float] = Field(None, description="The agent commission of the land", examples=[100])


class LandCreate(LandBase):
    crm_id: str = Field(None, description="The CRM ID of the land", examples=["L1"])
    responsible: Optional[str] = Field(None, description="The responsible person of the land", examples=["John Doe"])


class LandUpdate(LandBase):
    district: Optional[str] = Field(None, description="The district name of the land",
                                    examples=["Yunusabad"])
    title: Optional[str] = Field(None, min_length=3, max_length=50, description="The title of the land",
                                 examples=["Land for sale"])
    category: Optional[Category] = Field(None, description="The category of the land",
                                         examples=["LAND", "APARTMENT", "COMMERCIAL"])
    action_type: Optional[ActionType] = Field(None, description="The action type of the land",
                                              examples=["SALE", "RENT"])
    description: Optional[str] = Field(None, max_length=6000, description="The description of the land",
                                       examples=["Land for sale"])
    comment: Optional[str] = Field(None, max_length=6000, description="The comment of the land",
                                   examples=["Land for sale"])
    price: Optional[int] = Field(None, description="The price of the land", examples=[100000])
    rooms: Optional[int] = Field(None, description="The number of rooms in the land", examples=[1, 2, 3, 4, 5, 6])
    square_area: Optional[int] = Field(None, description="The square area of the land", examples=[100])
    floor_number: Optional[int] = Field(None, description="The floor number of the land", examples=[23])
    location: Optional[LocationLand] = Field(None, description="The location of the land", examples=["CITY", "SUBURB"])
    furnished: Optional[bool] = Field(None, description="The furnished status of the land", examples=[True, False])
    house_condition: Optional[HouseCondition] = Field(None, description="The house condition of the land",
                                                      examples=["EURO", "NORMAL", "REPAIR"])
    current_status: Optional[CurrentStatus] = Field(None, description='The current status of the apartment',
                                                    examples=['FREE', 'BUSY', 'SOON'])
    parking_place: Optional[bool] = Field(None, description="The parking place status of the land", examples=[True, False])
    agent_percent: Optional[int] = Field(..., description="The agent percent of the land", examples=[10])


class LandResponse(LandBase):
    id: int = Field(..., description="The ID of the land", examples=[1])
    crm_id: Optional[str] = Field(..., description="The CRM ID of the land", examples=["L1"])
    responsible: Optional[str] = Field(..., description="The responsible person of the land", examples=["John Doe"])
    media: Optional[List[LandMediaResponse]] = Field([], description="The media of the land")
    created_at: datetime.datetime = Field(..., description="The time the land was created",
                                          examples=["2021-08-01T12:00:00"])
    updated_at: datetime.datetime = Field(..., description="The time the land was updated",
                                          examples=["2021-08-01T12:00:00"])

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "crm_id": "L1",
                "district": "Yunusabad",
                "title": "Land for sale",
                "category": "LAND",
                "action_type": "SALE",
                "description": "Land for sale",
                "comment": "Land for sale",
                "price": 100000,
                "rooms": 1,
                "square_area": 100,
                "floor_number": 23,
                "location": "CITY",
                "furnished": True,
                "house_condition": "EURO",
                'current_status': 'FREE',
                "parking_place": True,
                "name": "John Doe",
                "phone_number": "+998901234567",
                "agent_percent": 10,
                "agent_commission": 100,
                "responsible": "John Doe",
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00",
                "media": [
                    {
                        "id": 1,
                        "url": "http://example.com/image.jpg",
                        "media_type": "image",
                        "land_id": 1,
                        "created_at": "2021-08-01T12:00:00",
                        "updated_at": "2021-08-01T12:00:00"
                    }
                ]
            }
        }
