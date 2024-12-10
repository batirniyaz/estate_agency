from sqlalchemy.orm import registry

from app.changes.funcs import register_event_listener


def register_event_listeners():
    mapper_registry = registry()
    for mapper in mapper_registry.mappers:
        model = mapper.class_
        register_event_listener(model)
