import datetime

from pydantic import BaseModel, Field, field_validator
from typing import Optional

from app.object.models import ActionType
from app.report.clients.model import ClientStatus, DealStatus


class ClientBase(BaseModel):
    action_type: ActionType = Field(..., description="The action type", examples=["SALE", "RENT"])
    responsible: str = Field(..., description="The responsible person of the client", examples=['Akobir'])
    client_name: str = Field(None, description="The name of the client", examples=['John'])
    date: str = Field(..., description="The date", examples=["2022-01-01"])
    district: list = Field([], description="The district", examples=[['Yunusabad', 'Mirzo Ulugbek']])
    budget: int = Field(None, description="The budget", examples=[100000])
    comment: str = Field(None, description="The comment", examples=['Good client'])
    client_status: ClientStatus = Field(None, description="The client status", examples=["HOT", "COLD"])
    deal_status: Optional[DealStatus] = Field(None, description="The deal status",
                             examples=["INITIAL_CONTACT", "NEGOTIATION", "DECISION_MAKING", "AGREEMENT_CONTACT", "DEAL"])

    @field_validator('date')
    def date_not_in_past(cls, v):
        if datetime.date.fromisoformat(v) > datetime.date.today():
            raise ValueError('Дата показа не может быть в будущем')
        return v


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    action_type: Optional[ActionType] = Field(None, description="The action type", examples=["SALE", "RENT"])
    responsible: Optional[str] = Field(None, description="The responsible person of the client", examples=['Akobir'])
    client_name: Optional[str] = Field(None, description="The name of the client", examples=['John'])
    date: Optional[str] = Field(None, description="The date", examples=["2022-01-01"])
    district: Optional[list] = Field(None, description="The district", examples=[['Yunusabad', 'Mirzo Ulugbek']])
    budget: Optional[int] = Field(None, description="The budget", examples=[100000])
    comment: Optional[str] = Field(None, description="The comment", examples=['Good client'])
    client_status: Optional[ClientStatus] = Field(None, description="The client status", examples=["HOT", "COLD"])
    deal_status: Optional[DealStatus] = Field(None, description="The deal status",
                                examples=["INITIAL_CONTACT", "NEGOTIATION", "DECISION_MAKING", "AGREEMENT_CONTACT", "DEAL"])



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
                "client_name": "John",
                "date": "2022-01-01",
                "district": ['Yunusabad', 'Mirzo Ulugbek'],
                "budget": 100000,
                "comment": "Good client",
                "client_status": "HOT",
                "deal_status": "INITIAL_CONTACT",
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }