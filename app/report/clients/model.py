# import datetime
#
# from sqlalchemy.orm import Mapped, mapped_column
# from sqlalchemy import Integer, String, Enum, TIMESTAMP, JSON
# from app.object.models import ActionType
# from enum import Enum as enumEnum
#
# from app.database import Base
#
#
# class ClientStatus(enumEnum):
#     HOT = 'hot'
#     COLD = 'cold'
#
#
# class DealStatus(enumEnum):
#     INITIAL_CONTACT = 'initial_contact'
#     NEGOTIATION = 'negotiation'
#     DECISION_MAKING = 'decision_making'
#     AGREEMENT_CONTACT = 'agreement_contract'
#     DEAL = 'deal'
#
#
# class Client(Base):
#     __tablename__ = 'client'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     action_type: Mapped[ActionType] = mapped_column(Enum(ActionType))
#     responsible: Mapped[str] = mapped_column(String)
#     client_name: Mapped[str] = mapped_column(String, nullable=True)
#     date: Mapped[str] = mapped_column(String)
#     district: Mapped[list] = mapped_column(JSON, default=[], nullable=True)
#     budget: Mapped[int] = mapped_column(Integer, nullable=True)
#     comment: Mapped[str] = mapped_column(String, nullable=True)
#     client_status: Mapped[ClientStatus] = mapped_column(Enum(ClientStatus), nullable=True)
#     deal_status: Mapped[DealStatus] = mapped_column(Enum(DealStatus), default=DealStatus.INITIAL_CONTACT, nullable=True)
#
#     created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
#                                                           default=lambda: datetime.datetime.now(datetime.timezone.utc))
#     updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
#                                                           default=lambda: datetime.datetime.now(datetime.timezone.utc),
#                                                           onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
