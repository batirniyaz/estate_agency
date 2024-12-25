import datetime

from pydantic import BaseModel, Field, field_validator
from typing import Optional

from app.object.models import ActionType


class ViewBase(BaseModel):
    action_type: ActionType = Field(..., description="The action type", examples=["SALE", "RENT"])
    responsible: str = Field(..., description="The responsible person of the view", examples=['Akobir'])
    date: str = Field(..., description="The date", examples=["2022-01-01"])
    time: str = Field(..., description="The time", examples=["12:00"])
    district: Optional[str] = Field(None, description="The district", examples=["Yunusabad"])
    price: int = Field(..., description="The price", examples=[100000])
    commission: float = Field(..., description="The commission", examples=[10000])
    agent_percent: int = Field(..., description="The agent percent", examples=[10])
    status_deal: bool = Field(False, description="The status deal", examples=[False])
    crm_id: str = Field(..., description="The CRM ID", examples=["A1"])
    client_number: Optional[str] = Field(None, max_length=13, description="The client number", examples=["+998901234567"])
    owner_number: Optional[str] = Field(None, max_length=13, description="The owner number", examples=["+998901234567"])

    @field_validator('date')
    def date_not_in_past(cls, v):
        if datetime.date.fromisoformat(v) > datetime.date.today():
            raise ValueError('Время показа не может быть в будущем')
        return v


class ViewCreate(ViewBase):
    pass


class ViewUpdate(ViewBase):
    action_type: Optional[ActionType] = Field(None, description="The action type", examples=["SALE", "RENT"])
    responsible: Optional[str] = Field(None, description="The responsible person of the view", examples=['Akobir'])
    date: Optional[str] = Field(None, description="The date", examples=["2022-01-01"])
    time: Optional[str] = Field(None, description="The time", examples=["12:00"])
    district: Optional[str] = Field(None, description="The district", examples=["Yunusabad"])
    price: Optional[int] = Field(None, description="The price", examples=[100000])
    commission: Optional[float] = Field(None, description="The commission", examples=[10000])
    agent_percent: Optional[int] = Field(None, description="The agent percent", examples=[10])
    status_deal: Optional[bool] = Field(None, description="The status deal", examples=[False])
    crm_id: Optional[str] = Field(None, description="The CRM ID", examples=["A1"])
    client_number: Optional[str] = Field(None, max_length=13, description="The client number", examples=["+998901234567"])
    owner_number: Optional[str] = Field(None, max_length=13, description="The owner number", examples=["+998901234567"])


class ViewResponse(ViewBase):
    id: int = Field(..., description="The ID of the view", examples=[1])
    created_at: datetime.datetime = Field(..., description="The time the view was created",
                                          examples=["2021-08-01T12:00:00"])
    updated_at: datetime.datetime = Field(..., description="The time the view was updated",
                                          examples=["2021-08-01T12:00:00"])

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "action_type": "SALE",
                "responsible": "Akobir",
                "date": "2022-01-01",
                "time": "12:00",
                "district": "Yunusabad",
                "price": 100000,
                "commission": 10000,
                "agent_percent": 10,
                "status_deal": False,
                "crm_id": "A1",
                "client_number": "+998901234567",
                "owner_number": "+998901234567",
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }