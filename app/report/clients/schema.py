import datetime

from pydantic import BaseModel, Field, field_validator
from typing import Optional

from app.object.models import ActionType


class ClientBase(BaseModel):
    action_type: ActionType = Field(..., description="The action type", examples=["SALE", "RENT"])
    responsible: str = Field(..., description="The responsible person of the client", examples=['Akobir'])
    date: str = Field(..., description="The date", examples=["2022-01-01"])
    hot_clients: int = Field(..., description="The number of hot clients", examples=[10])
    cold_clients: int = Field(..., description="The number of cold clients", examples=[10])
    calls: int = Field(..., description="The number of calls", examples=[10])

    @field_validator('date')
    def date_not_in_past(cls, v):
        if datetime.date.fromisoformat(v) < datetime.date.today():
            raise ValueError('Date cannot be in the past')
        return v


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    action_type: Optional[ActionType] = Field(None, description="The action type", examples=["SALE", "RENT"])
    responsible: Optional[str] = Field(None, description="The responsible person of the client", examples=['Akobir'])
    date: Optional[str] = Field(None, description="The date", examples=["2022-01-01"])
    hot_clients: Optional[int] = Field(None, description="The number of hot clients", examples=[10])
    cold_clients: Optional[int] = Field(None, description="The number of cold clients", examples=[10])
    calls: Optional[int] = Field(None, description="The number of calls", examples=[10])


class ClientResponse(ClientBase):
    id: int = Field(..., description="The ID of the client", examples=[1])
    created_at: datetime.datetime = Field(..., description="The time the client was created",
                                          examples=["2021-08-01T12:00:00"])
    updated_at: datetime.datetime = Field(..., description="The time the client was updated",
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
                "hot_clients": 10,
                "cold_clients": 10,
                "calls": 10,
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }