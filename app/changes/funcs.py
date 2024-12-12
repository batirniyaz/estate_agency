import asyncio
from typing import Type, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.event import listens_for
from app.changes.model import ChangeLog, OperationType

log_queue = asyncio.Queue()


def serialize(data):
    if data is None:
        return None
    return {key: (value.isoformat() if isinstance(value, datetime) else value.value if isinstance(value, Enum) else value) for key, value in data.items()}


async def log_change(db: AsyncSession, table_name: str, operation: OperationType, user: str, before_data: dict, after_data: dict):
    try:
        change_log = ChangeLog(
            table_name=table_name,
            operation=operation,
            before_data=before_data,
            after_data=after_data,
            user_id=user_id,
        )
        db.add(change_log)
        await db.commit()
        await db.refresh(change_log)
    except Exception as e:
        await db.rollback()
        raise e


async def process_log_queue():
    while True:
        db_session, table_name, operation, user_id, before_data, after_data = await log_queue.get()
        try:
            await log_change(db_session, table_name, operation, user_id, before_data, after_data)
        except Exception as e:
            print(f"Failed to log change for {table_name}, operation {operation}, user {user_id}: {e}")
        finally:
            log_queue.task_done()


def register_event_listener(model: Type):
    @listens_for(model, 'before_update')
    def capture_before_update(mapper, connection, target):
        target._before_update = {column.key: getattr(target, column.key) for column in mapper.columns}

    @listens_for(model, 'after_update')
    def receive_after_update(mapper, connection, target):
        db_session = AsyncSession.object_session(target)
        if db_session:
            asyncio.create_task(
                log_queue.put((db_session, model.__tablename__, OperationType.UPDATE, target.created_by_id,
                               getattr(target, '_before_update', {}),
                               {column.key: getattr(target, column.key) for column in mapper.columns}))
            )

    @listens_for(model, 'after_insert')
    def receive_after_insert(mapper, connection, target):
        db_session = AsyncSession.object_session(target)
        if db_session:
            asyncio.create_task(
                log_queue.put((db_session, model.__tablename__, OperationType.CREATE, target.created_by_id,
                               None,
                               {column.key: getattr(target, column.key) for column in mapper.columns}))
            )

    @listens_for(model, 'after_delete')
    def receive_after_delete(mapper, connection, target):
        db_session = AsyncSession.object_session(target)
        if db_session:
            asyncio.create_task(
                log_queue.put((db_session, model.__tablename__, OperationType.DELETE, target.created_by_id,
                               {column.key: getattr(target, column.key) for column in mapper.columns},
                               None))
            )
