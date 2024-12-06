from pydantic import BaseModel, Field
import datetime
from typing import List, Optional

from app.object.models import Category, ActionType, LocationCommercial, HouseCondition, CurrentStatus


class CommercialMediaResponse(BaseModel):
    id: int = Field(..., description="The ID of the image", examples=[1])
    url: str = Field(..., description="The URL of the image", examples=["http://example.com/image.jpg"])
    media_type: str = Field(..., description="Tcommercial type of the media", examples=["image"])
    commercial_id: int = Field(..., description="The ID of the commercial", examples=[1])
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
                "commercial_id": 1,
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }


class CommercialBase(BaseModel):
    district: str = Field(..., description="The district name of the commercial",
                          examples=["Yunusabad"])
    title: str = Field(..., min_length=3, max_length=50, description="The title of the commercial",
                       examples=["Commercial for sale"])
    category: Category = Field(..., description="The category of the commercial",
                               examples=["COMMERCIAL", "APARTMENT", "LAND"])
    action_type: ActionType = Field(..., description="The action type of the commercial",
                                    examples=["SALE", "RENT"])
    description: Optional[str] = Field(None, max_length=6000, description="The description of the commercial", examples=["Commercial for sale"])
    comment: Optional[str] = Field(None, max_length=6000, description="The comment of the commercial", examples=["Commercial for sale"])
    price: int = Field(..., description="The price of the commercial", examples=[100000])
    rooms: int = Field(..., description="The number of rooms in the commercial", examples=[1, 2, 3, 4, 5, 6])
    square_area: int = Field(..., description="The square area of the commercial", examples=[100])
    floor_number: int = Field(..., description="The floor number of the commercial", examples=[23])
    location: LocationCommercial = Field(..., description="The location of the commercial", examples=["CITY", "SUBURB"])
    furnished: bool = Field(True, description="The furnished status of the commercial", examples=[True, False])
    house_condition: HouseCondition = Field(..., description="The house condition of the commercial",
                                            examples=["EURO", "NORMAL", "REPAIR"])
    current_status: CurrentStatus = Field(None, description='The current status of the apartment',
                                          examples=['FREE', 'BUSY', 'SOON'])
    parking_place: bool = Field(..., description="The parking place status of the commercial", examples=[True, False])
    agent_percent: Optional[int] = Field(..., description="The agent percent of the commercial", examples=[10])
    agent_commission: Optional[float] = Field(None, description="The agent commission of the commercial", examples=[100])


class CommercialCreate(CommercialBase):
    crm_id: str = Field(None, description="The CRM ID of the commercial", examples=["C1"])
    responsible: Optional[str] = Field(None, description="The responsible person of the commercial", examples=["John Doe"])


class CommercialUpdate(CommercialBase):
    district: Optional[str] = Field(None, description="The district name of the commercial",
                                    examples=["Yunusabad"])
    title: Optional[str] = Field(None, min_length=3, max_length=50, description="The title of the commercial",
                                 examples=["Land for sale"])
    category: Optional[Category] = Field(None, description="The category of the commercial",
                                         examples=["LAND", "APARTMENT", "COMMERCIAL"])
    action_type: Optional[ActionType] = Field(None, description="The action type of the commercial",
                                              examples=["SALE", "RENT"])
    description: Optional[str] = Field(None, max_length=6000, description="The description of the commercial",
                                       examples=["Commercial for sale"])
    comment: Optional[str] = Field(None, max_length=6000, description="The comment of the commercial",
                                   examples=["Commercial for sale"])
    price: Optional[int] = Field(None, description="The price of the commercial", examples=[100000])
    rooms: Optional[int] = Field(None, description="The number of rooms in the commercial", examples=[1, 2, 3, 4, 5, 6])
    square_area: Optional[int] = Field(None, description="The square area of the commercial", examples=[100])
    floor_number: Optional[int] = Field(None, description="The floor number of the commercial", examples=[23])
    location: Optional[LocationCommercial] = Field(None, description="The location of the commercial", examples=["CITY", "SUBURB"])
    furnished: Optional[bool] = Field(None, description="The furnished status of the commercial", examples=[True, False])
    house_condition: Optional[HouseCondition] = Field(None, description="The house condition of the commercial",
                                                      examples=["EURO", "NORMAL", "REPAIR"])
    current_status: Optional[CurrentStatus] = Field(None, description='The current status of the apartment',
                                                    examples=['FREE', 'BUSY', 'SOON'])
    parking_place: Optional[bool] = Field(None, description="The parking place status of the commercial", examples=[True, False])
    agent_percent: Optional[int] = Field(..., description="The agent percent of the commercial", examples=[10])


class CommercialResponse(CommercialBase):
    id: int = Field(..., description="The ID of the commercial", examples=[1])
    crm_id: Optional[str] = Field(..., description="The CRM ID of the commercial", examples=["C1"])
    responsible: Optional[str] = Field(..., description="The responsible person of the commercial", examples=["John Doe"])
    media: Optional[List[CommercialMediaResponse]] = Field([], description="The media of the commercial")
    created_at: datetime.datetime = Field(..., description="The time the commercial was created",
                                          examples=["2021-08-01T12:00:00"])
    updated_at: datetime.datetime = Field(..., description="The time the commercial was updated",
                                          examples=["2021-08-01T12:00:00"])

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "crm_id": "C1",
                "district": "Yunusabad",
                "title": "Commercial for sale",
                "category": "COMMERCIAL",
                "action_type": "SALE",
                "description": "Commercial for sale",
                "comment": "Commercial for sale",
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
                        "commercial_id": 1,
                        "created_at": "2021-08-01T12:00:00",
                        "updated_at": "2021-08-01T12:00:00"
                    }
                ]
            }
        }


