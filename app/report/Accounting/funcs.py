from datetime import datetime, timedelta

from fastapi import HTTPException, status
from typing import Optional

from sqlalchemy import func, extract
from sqlalchemy.future import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.object.models import ActionType
from app.object.models.apartment import Apartment
from app.object.models.commercial import Commercial
from app.object.models.land import Land
from app.report.clients.model import Client, ClientStatus
from app.report.deals.model import Deal
from app.report.views.model import View


async def get_counts_by_month(db):
    months = {
        "jan": {"sale": 0, "rent": 0},
        "feb": {"sale": 0, "rent": 0},
        "mar": {"sale": 0, "rent": 0},
        "apr": {"sale": 0, "rent": 0},
        "may": {"sale": 0, "rent": 0},
        "jun": {"sale": 0, "rent": 0},
        "jul": {"sale": 0, "rent": 0},
        "aug": {"sale": 0, "rent": 0},
        "sep": {"sale": 0, "rent": 0},
        "oct": {"sale": 0, "rent": 0},
        "nov": {"sale": 0, "rent": 0},
        "dec": {"sale": 0, "rent": 0},
    }

    async def process_query(model):
        query = select(
            extract('month', model.created_at).label('month'),
            model.action_type,
            func.count(model.id).label('count')
        ).group_by(
            extract('month', model.created_at),
            model.action_type
        )
        results = await db.execute(query)
        return results.all()

    data_land = await process_query(Land)
    data_commercial = await process_query(Commercial)
    data_apartment = await process_query(Apartment)

    all_data = data_land + data_commercial + data_apartment

    for row in all_data:
        month = int(row.month)
        action_type = row.action_type.name.lower()
        count = row.count

        month_name = list(months.keys())[month - 1]
        months[month_name][action_type] += count

    totals = {}
    for month, values in months.items():
        totals[month] = values["sale"] + values["rent"]

    return months, totals


async def get_overall_data(
    db: AsyncSession,
    action_type: ActionType,
    current_user,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    date: Optional[str] = None,
    responsible: Optional[str] = None,
):
    print(start_date, end_date, date)
    if start_date and not end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Требуется указать дату окончания")
    if end_date and not start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Требуется указать дату начала")
    if date and (start_date or end_date):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нельзя указать дату и диапазон дат")

    deal_query = select(Deal).filter_by(action_type=action_type)
    view_query = select(View).filter_by(action_type=action_type)
    client_query = select(Client).filter_by(action_type=action_type)

    land_query = select(Land).filter_by(action_type=action_type)
    apartment_query = select(Apartment).filter_by(action_type=action_type)
    commercial_query = select(Commercial).filter_by(action_type=action_type)

    if date:
        date_obj = datetime.strptime(date, '%Y-%m-%d' if len(date) == 10 else '%Y-%m' if len(date) == 7 else '%Y')

        if len(date) == 10:
            deal_query = deal_query.filter(Deal.date == date)
            view_query = view_query.filter(View.date == date)
            client_query = client_query.filter(Client.date == date)

        elif len(date) == 7:
            deal_query = deal_query.filter(Deal.date.like(f'{date}-%'))
            view_query = view_query.filter(View.date.like(f'{date}-%'))
            client_query = client_query.filter(Client.date.like(f'{date}-%'))

        elif len(date) == 4:
            deal_query = deal_query.filter(Deal.date.like(f'{date}-%'))
            view_query = view_query.filter(View.date.like(f'{date}-%'))
            client_query = client_query.filter(Client.date.like(f'{date}-%'))

        elif len(date) == 8 and date[5] == 'W':
            year, week = int(date[:4]), int(date[6:])
            start_of_week = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
            end_of_week = start_of_week + timedelta(days=6)
            deal_query = deal_query.filter(Deal.date >= start_of_week.strftime('%Y-%m-%d'),
                                 Deal.date <= end_of_week.strftime('%Y-%m-%d'))
            view_query = view_query.filter(View.date >= start_of_week.strftime('%Y-%m-%d'),
                                    View.date <= end_of_week.strftime('%Y-%m-%d'))
            client_query = client_query.filter(Client.date >= start_of_week.strftime('%Y-%m-%d'),
                                    Client.date <= end_of_week.strftime('%Y-%m-%d'))

        land_query = land_query.filter(Land.created_at == date_obj)
        apartment_query = apartment_query.filter(Apartment.created_at == date_obj)
        commercial_query = commercial_query.filter(Commercial.created_at == date_obj)


    elif start_date and end_date:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d' if len(start_date) == 10 else '%Y-%m' if len(
            start_date) == 7 else '%Y')
        end_date_obj = datetime.strptime(end_date,
                                         '%Y-%m-%d' if len(end_date) == 10 else '%Y-%m' if len(end_date) == 7 else '%Y')

        if start_date_obj > end_date_obj:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Дата начала не может быть больше даты окончания")

        if len(start_date) == 10 and len(end_date) == 10:
            deal_query = deal_query.filter(Deal.date >= start_date, Deal.date <= end_date)
            view_query = view_query.filter(View.date >= start_date, View.date <= end_date)
            client_query = client_query.filter(Client.date >= start_date, Client.date <= end_date)

            land_query = land_query.filter(Land.created_at >= start_date_obj, Land.created_at <= end_date_obj)
            apartment_query = apartment_query.filter(Apartment.created_at >= start_date_obj,
                                                     Apartment.created_at <= end_date_obj)
            commercial_query = commercial_query.filter(Commercial.created_at >= start_date_obj,
                                                       Commercial.created_at <= end_date_obj)

        elif len(start_date) == 7 and len(end_date) == 7:
            start_date_obj = datetime.strptime(start_date, '%Y-%m')
            end_date_obj = datetime.strptime(end_date, '%Y-%m')
            end_date_obj = end_date_obj.replace(day=1) + timedelta(days=32)
            end_date_obj = end_date_obj.replace(day=1) - timedelta(days=1)
            deal_query = deal_query.filter(Deal.date >= start_date_obj.strftime('%Y-%m-%d'),
                                           Deal.date <= end_date_obj.strftime('%Y-%m-%d'))
            view_query = view_query.filter(View.date >= start_date_obj.strftime('%Y-%m-%d'),
                                           View.date <= end_date_obj.strftime('%Y-%m-%d'))
            client_query = client_query.filter(Client.date >= start_date_obj.strftime('%Y-%m-%d'),
                                           Client.date <= end_date_obj.strftime('%Y-%m-%d'))

            land_query = land_query.filter(Land.created_at >= start_date_obj, Land.created_at <= end_date_obj)
            apartment_query = apartment_query.filter(Apartment.created_at >= start_date_obj,
                                                     Apartment.created_at <= end_date_obj)
            commercial_query = commercial_query.filter(Commercial.created_at >= start_date_obj,
                                                       Commercial.created_at <= end_date_obj)


        elif len(start_date) == 4 and len(end_date) == 4:
            start_date_obj = datetime.strptime(start_date, '%Y')
            end_date_obj = datetime.strptime(end_date, '%Y')
            end_date_obj = end_date_obj.replace(month=12, day=31)
            deal_query = deal_query.filter(Deal.date >= start_date_obj.strftime('%Y-%m-%d'),
                                           Deal.date <= end_date_obj.strftime('%Y-%m-%d'))
            view_query = view_query.filter(View.date >= start_date_obj.strftime('%Y-%m-%d'),
                                           View.date <= end_date_obj.strftime('%Y-%m-%d'))
            client_query = client_query.filter(Client.date >= start_date_obj.strftime('%Y-%m-%d'),
                                             Client.date <= end_date_obj.strftime('%Y-%m-%d'))
            land_query = land_query.filter(Land.created_at >= start_date_obj, Land.created_at <= end_date_obj)
            apartment_query = apartment_query.filter(Apartment.created_at >= start_date_obj,
                                                     Apartment.created_at <= end_date_obj)
            commercial_query = commercial_query.filter(Commercial.created_at >= start_date_obj,
                                                       Commercial.created_at <= end_date_obj)

    if not responsible:
        if not current_user.id == 11:
            responsible = current_user.full_name

    if responsible:
        if not current_user.id == 11:
            deal_query = deal_query.filter(Deal.responsible == responsible)
            view_query = view_query.filter(View.responsible == responsible)
            client_query = client_query.filter(Client.responsible == responsible)
            land_query = land_query.filter(Land.responsible == responsible)
            apartment_query = apartment_query.filter(Apartment.responsible == responsible)
            commercial_query = commercial_query.filter(Commercial.responsible == responsible)

    db_deals = await db.execute(deal_query)
    db_views = await db.execute(view_query)
    db_clients = await db.execute(client_query)
    db_lands = await db.execute(land_query)
    db_apartments = await db.execute(apartment_query)
    db_commercials = await db.execute(commercial_query)

    deals = db_deals.scalars().all()
    views = db_views.scalars().all()
    clients = db_clients.scalars().all()
    lands = db_lands.scalars().all()
    apartments = db_apartments.scalars().all()
    commercials = db_commercials.scalars().all()

    months, total = await get_counts_by_month(db)
    print(current_user.full_name)
    print(responsible)

    # if current_user.id == 11 and responsible == current_user.full_name:
    #     commission_count = sum(deal.agency_commission for deal in deals if deal.agency_commission is not None)
    if current_user.id == 11:
        commission_count = sum(deal.agency_commission for deal in deals if deal.agency_commission is not None)
    else:
        print("I am in three")
        commission_count = sum([deal.commission for deal in deals])

    return {
        "deals": deals, "deals_count": len(deals), "views": views, "views_count": len(views),
        "clients": clients, "clients_count": len(clients), "commission_count": commission_count,
        "hot_count": len([client for client in clients if client.client_status == ClientStatus.HOT]),
        "cold_count": len([client for client in clients if client.client_status == ClientStatus.COLD]),
        "all_objects": len(lands) + len(apartments) + len(commercials), "months": months, "total": total
    }
