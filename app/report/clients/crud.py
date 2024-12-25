from signal import valid_signals

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.report.clients.model import Client
from app.report.clients.schema import ClientCreate, ClientUpdate
from app.report.validations.client_validate import validate_client


async def create_client(db: AsyncSession, client: ClientCreate):

    await validate_client(db, client)
    if client.action_type == 'sale' and not client.deal_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Статус сделки обязателен для продажи")
    else:
        client.deal_status = None

    try:

        db_client = Client(**client.model_dump())
        db.add(db_client)
        await db.commit()
        await db.refresh(db_client)
        return db_client
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_clients(db: AsyncSession, limit: int = 10, page: int = 1):
    res = await db.execute(select(Client).limit(limit).offset((page - 1) * limit))
    clients = res.scalars().all()
    total_count = await db.scalar(select(func.count(Client.id)))

    return {"data": clients or [], "total_count": total_count}


async def get_client(db: AsyncSession, client_id: int):
    res = await db.execute(select(Client).filter_by(id=client_id))
    client = res.scalars().first()

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найден")

    return client


async def update_client(db: AsyncSession, client_id: int, client: ClientUpdate):
    await validate_client(db, client)
    db_client = await get_client(db, client_id)

    try:

        for key, value in client.model_dump(exclude_unset=True).items():
            setattr(db_client, key, value)

        await db.commit()
        await db.refresh(db_client)
        return db_client
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_client(db: AsyncSession, client_id: int):
    db_client = await get_client(db, client_id)
    try:
        await db.delete(db_client)
        await db.commit()
        return {"message": "Клиент успешно удален"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))