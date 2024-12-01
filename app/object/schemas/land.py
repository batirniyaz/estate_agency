from fastapi import UploadFile, File
from pydantic import BaseModel, Field
import datetime
from typing import List, Optional

from app.object.models import Category, ActionType, HouseType, BathroomType, HouseCondition


class LandImageCreate(BaseModel):
    file: UploadFile = File(..., description="The image file to upload")


class LandImageUpdate(LandImageCreate):
    pass


class LandMediaResponse(BaseModel):
    id: int = Field(..., description="The ID of the image", examples=[1])
    url: str = Field(..., description="The URL of the image", examples=["http://example.com/image.jpg"])
    land_id: int = Field(..., description="The ID of the land", examples=[1])
    created_at: datetime.datetime = Field(..., description="The time the image was created",
                                          examples=["2021-08-01T12:00:00"])
    updated_at: datetime.datetime = Field(..., description="The time the image was updated",
                                          examples=["2021-08-01T12:00:00"])


class LandBase(BaseModel):
    district: str = Field(..., min_length=3, max_length=100, description="The district name of the land",
                          examples=["Yunusabad"])
    metro_st: str = Field(..., min_length=3, max_length=100, description="The name of the nearest metro station",
                          examples=["Buyuk Ipak Yuli"])
    title: str = Field(..., min_length=3, max_length=100, description="The title of the land",
                       examples=["Land for sale"])
    category: Category = Field(..., min_length=3, max_length=100, description="The category of the land",
                               examples=["LAND", "APARTMENT", "COMMERCIAL"])
    action_type: ActionType = Field(..., min_length=3, max_length=100, description="The action type of the land",
                                    examples=["SALE", "RENT"])
    description: str = Field(..., min_length=3, description="The description of the land", examples=["Land for sale"])
    comment: str = Field(..., min_length=3, description="The comment of the land", examples=["Land for sale"])
    price: int = Field(..., description="The price of the land", examples=[100000])
    house_type: HouseType = Field(..., min_length=3, max_length=100, description="The house type of the land",
                                  examples=["NEW_BUILDING", "SECONDARY"])
    rooms: int = Field(..., description="The number of rooms in the land", examples=[1, 2, 3, 4, 5, 6])
    square_area: int = Field(..., description="The square area of the land", examples=[100])
    floor_number: int = Field(..., description="The floor number of the land", examples=[23])
    floor: int = Field(..., description="The floor of the land", examples=[10])
    bathroom: BathroomType = Field(..., min_length=3, max_length=100, description="The bathroom type of the land",
                                   examples=["SEPERATED", "COMBINED", "MANY"])
    furnished: bool = Field(..., description="The furnished status of the land", examples=[True, False])
    house_condition: HouseCondition = Field(..., min_length=3, max_length=100,
                                            description="The house condition of the land",
                                            examples=["EURO", "NORMAL", "REPAIR"])
    name: str = Field(..., min_length=3, max_length=100, description="The name of the contact person",
                      examples=["John Doe"])
    phone_number: str = Field(..., min_length=3, max_length=100, description="The phone number of the contact person",
                              examples=["+998901234567"])
    agent_percent: Optional[int] = Field(..., description="The agent percent of the land", examples=[10])


class LandCreate(LandBase):
    pass


class LandUpdate(LandBase):
    district: Optional[str] = Field(None, min_length=3, max_length=100, description="The district name of the land",
                                    examples=["Yunusabad"])
    metro_st: Optional[str] = Field(None, min_length=3, max_length=100,
                                    description="The name of the nearest metro station", examples=["Buyuk Ipak Yuli"])
    title: Optional[str] = Field(None, min_length=3, max_length=100, description="The title of the land",
                                 examples=["Land for sale"])
    category: Optional[Category] = Field(None, min_length=3, max_length=100, description="The category of the land",
                                         examples=["LAND", "APARTMENT", "COMMERCIAL"])
    action_type: Optional[ActionType] = Field(None, min_length=3, max_length=100,
                                              description="The action type of the land", examples=["SALE", "RENT"])
    description: Optional[str] = Field(None, min_length=3, description="The description of the land",
                                       examples=["Land for sale"])
    comment: Optional[str] = Field(None, min_length=3, description="The comment of the land",
                                   examples=["Land for sale"])
    price: Optional[int] = Field(None, description="The price of the land", examples=[100000])
    house_type: Optional[HouseType] = Field(None, min_length=3, max_length=100,
                                            description="The house type of the land",
                                            examples=["NEW_BUILDING", "SECONDARY"])
    rooms: Optional[int] = Field(None, description="The number of rooms in the land", examples=[1, 2, 3, 4, 5, 6])
    square_area: Optional[int] = Field(None, description="The square area of the land", examples=[100])
    floor_number: Optional[int] = Field(None, description="The floor number of the land", examples=[23])
    floor: Optional[int] = Field(None, description="The floor of the land", examples=[10])
    bathroom: Optional[BathroomType] = Field(None, min_length=3, max_length=100,
                                             description="The bathroom type of the land",
                                             examples=["SEPERATED", "COMBINED", "MANY"])
    furnished: Optional[bool] = Field(None, description="The furnished status of the land", examples=[True, False])
    house_condition: Optional[HouseCondition] = Field(None, min_length=3, max_length=100,
                                                      description="The house condition of the land",
                                                      examples=["EURO", "NORMAL", "REPAIR"])
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="The name of the contact person",
                                examples=["John Doe"])
    phone_number: Optional[str] = Field(None, min_length=3, max_length=100,
                                        description="The phone number of the contact person",
                                        examples=["+998901234567"])
    agent_percent: Optional[int] = Field(None, description="The agent percent of the land", examples=[10])


class LandResponse(LandBase):
    id: int = Field(..., description="The ID of the land", examples=[1])
    media: List[LandMediaResponse] = Field(..., description="The images of the land")
    responsible: Optional[str] = Field(None, min_length=3, max_length=100,
                                       description="The name of the responsible person", examples=["John Doe"])
    created_at: datetime.datetime = Field(..., description="The created date of the land",
                                          examples=["2022-01-01T00:00:00"])
    updated_at: datetime.datetime = Field(..., description="The updated date of the land",
                                          examples=["2022-01-01T00:00:00"])
