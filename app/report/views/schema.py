import datetime

from pydantic import BaseModel, Field, field_validator
from typing import Optional

from app.object.models import ActionType


class ViewBase(BaseModel):
    action_type: ActionType = Field(..., description="The action type", examples=["SALE", "RENT"])
    responsible: str = Field(..., description="The responsible person of the view", examples=['Akobir'])
    date: str = Field(..., description="The date", examples=["2022-01-01"])
    object_sum: int = Field(..., description="The number of objects", examples=[10])
    commission_sum: int = Field(..., description="The commission sum", examples=[1000])
    agent_percent: int = Field(..., description="The agent percent", examples=[10])
    crm_id: str = Field(..., description="The CRM ID", examples=["A1"])

    @field_validator('date')
    def date_not_in_past(cls, v):
        if datetime.date.fromisoformat(v) < datetime.date.today():
            raise ValueError('Date cannot be in the past')
        return v


class ViewCreate(ViewBase):
    pass


class ViewUpdate(ViewBase):
    action_type: Optional[ActionType] = Field(None, description="The action type", examples=["SALE", "RENT"])
    responsible: Optional[str] = Field(None, description="The responsible person of the view", examples=['Akobir'])
    date: Optional[str] = Field(None, description="The date", examples=["2022-01-01"])
    object_sum: Optional[int] = Field(None, description="The number of objects", examples=[10])
    commission_sum: Optional[int] = Field(None, description="The commission sum", examples=[1000])
    agent_percent: Optional[int] = Field(None, description="The agent percent", examples=[10])
    crm_id: Optional[str] = Field(None, description="The CRM ID", examples=["A1"])


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
                "object_sum": 10,
                "commission_sum": 1000,
                "agent_percent": 10,
                "crm_id": "A1",
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }