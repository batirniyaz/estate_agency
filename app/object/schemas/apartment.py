from pydantic import BaseModel, Field
import datetime
from typing import List, Optional

from app.object.models import Category, ActionType, HouseType, BathroomType, HouseCondition, CurrentStatus


class ApartmentMediaResponse(BaseModel):
    id: int = Field(..., description="The ID of the image", examples=[1])
    url: str = Field(..., description="The URL of the image", examples=["http://example.com/image.jpg"])
    media_type: str = Field(..., description="The type of the media", examples=["image"])
    apartment_id: int = Field(..., description="The ID of the apartment", examples=[1])
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
                "apartment_id": 1,
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }


class ApartmentBase(BaseModel):
    district: str = Field(..., description="The district name of the apartment",
                          examples=["Yunusabad"])
    metro_st: Optional[str] = Field(None, description="The name of the nearest metro station",
                          examples=["Buyuk Ipak Yuli"])
    title: str = Field(..., min_length=3, max_length=50, description="The title of the apartment",
                       examples=["Apartment for sale"])
    category: Category = Field(..., description="The category of the apartment",
                               examples=["APARTMENT", "LAND", "COMMERCIAL"])
    action_type: ActionType = Field(..., description="The action type of the apartment",
                                    examples=["SALE", "RENT"])
    description: Optional[str] = Field(None, max_length=6000, description="The description of the apartment", examples=["Apartment for sale"])
    comment: Optional[str] = Field(None, max_length=6000, description="The comment of the apartment", examples=["Apartment for sale"])
    price: int = Field(..., description="The price of the apartment", examples=[100000])
    house_type: HouseType = Field(..., description="The house type of the apartment",
                                  examples=["NEW_BUILDING", "SECONDARY"])
    rooms: int = Field(..., description="The number of rooms in the apartment", examples=[1, 2, 3, 4, 5, 6])
    square_area: int = Field(..., description="The square area of the apartment", examples=[100])
    floor_number: int = Field(..., description="The floor number of the apartment", examples=[23])
    floor: int = Field(..., description="The floor of the apartment", examples=[10])
    bathroom: BathroomType = Field(..., description="The bathroom type of the apartment",
                                   examples=["SEPERATED", "COMBINED", "MANY"])
    furnished: bool = Field(True, description="The furnished status of the apartment", examples=[True, False])
    house_condition: HouseCondition = Field(..., description="The house condition of the apartment",
                                            examples=["EURO", "NORMAL", "REPAIR"])
    current_status: CurrentStatus = Field(..., description='The current status of the apartment',
                                          examples=['FREE', 'BUSY', 'SOON'])
    status_date: Optional[str] = Field(None, description="The status date of the apartment", examples=["2022-01-01"])
    name: str = Field(..., min_length=3, max_length=100, description="The name of the contact person",
                      examples=["John Doe"])
    phone_number: str = Field(..., min_length=3, max_length=13, description="The phone number of the contact person",
                              examples=["+998901234567"])
    agent_percent: Optional[int] = Field(..., description="The agent percent of the apartment", examples=[10])
    agent_commission: Optional[float] = Field(None, description="The agent commission of the apartment", examples=[100])
    second_responsible: Optional[str] = Field(None, max_length=100)
    second_agent_percent: Optional[int] = Field(None, description="The second agent percent of the apartment", examples=[10])
    second_agent_commission: Optional[float] = Field(None, description="The second agent commission of the apartment",
                                                     examples=[100])
    deal: bool = Field(False, description="The deal status of the apartment", examples=[True, False])


class ApartmentCreate(ApartmentBase):
    crm_id: str = Field(None, max_length=255, description="The CRM ID of the apartment")
    responsible: Optional[str] = Field(None, max_length=100)


class ApartmentUpdate(ApartmentBase):
    district: Optional[str] = Field(None, description="The district name of the apartment",
                                    examples=["Yunusabad"])
    metro_st: Optional[str] = Field(None,
                                    description="The name of the nearest metro station", examples=["Buyuk Ipak Yuli"])
    title: Optional[str] = Field(None, min_length=3, max_length=100, description="The title of the apartment",
                                 examples=["apartment for sale"])
    category: Optional[Category] = Field(None, description="The category of the apartment",
                                         examples=["LAND", "APARTMENT", "COMMERCIAL"])
    action_type: Optional[ActionType] = Field(None, description="The action type of the apartment", examples=["SALE", "RENT"])
    description: Optional[str] = Field(None, max_length=6000, description="The description of the apartment",
                                       examples=["apartment for sale"])
    comment: Optional[str] = Field(None, max_length=6000, description="The comment of the apartment",
                                   examples=["apartment for sale"])
    price: Optional[int] = Field(None, description="The price of the apartment", examples=[100000])
    house_type: Optional[HouseType] = Field(None, description="The house type of the apartment",
                                            examples=["NEW_BUILDING", "SECONDARY"])
    rooms: Optional[int] = Field(None, description="The number of rooms in the apartment", examples=[1, 2, 3, 4, 5, 6])
    square_area: Optional[int] = Field(None, description="The square area of the apartment", examples=[100])
    floor_number: Optional[int] = Field(None, description="The floor number of the apartment", examples=[23])
    floor: Optional[int] = Field(None, description="The floor of the apartment", examples=[10])
    bathroom: Optional[BathroomType] = Field(None, description="The bathroom type of the apartment",
                                             examples=["SEPERATED", "COMBINED", "MANY"])
    furnished: Optional[bool] = Field(None, description="The furnished status of the apartment", examples=[True, False])
    house_condition: Optional[HouseCondition] = Field(None, description="The house condition of the apartment",
                                                      examples=["EURO", "NORMAL", "REPAIR"])
    current_status: Optional[CurrentStatus] = Field(None, description='The current status of the apartment',
                                                    examples=['FREE', 'BUSY', 'SOON'])
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="The name of the contact person",
                                examples=["John Doe"])
    phone_number: Optional[str] = Field(None, min_length=3, max_length=13,
                                        description="The phone number of the contact person",
                                        examples=["+998901234567"])
    agent_percent: Optional[int] = Field(None, description="The agent percent of the apartment", examples=[10])


class ApartmentResponse(ApartmentBase):
    id: int = Field(..., description="The ID of the apartment", examples=[1])
    crm_id: Optional[str] = Field(..., max_length=255, description="The CRM ID of the apartment", examples=["A1"])
    media: Optional[List[ApartmentMediaResponse]] = Field(None, description="The images of the apartment")
    responsible: Optional[str] = Field(None, min_length=3, max_length=100,
                                       description="The name of the responsible person", examples=["John Doe"])
    agent_commission: Optional[float] = Field(None, description="The agent commission of the apartment", examples=[100])
    created_at: datetime.datetime = Field(..., description="The created date of the apartment",
                                          examples=["2022-01-01T00:00:00"])
    updated_at: datetime.datetime = Field(..., description="The updated date of the apartment",
                                          examples=["2022-01-01T00:00:00"])

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        use_enum_values = True
