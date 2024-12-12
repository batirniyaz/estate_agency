
from app.changes.funcs import register_event_listener

from app.object.models.land import Land
from app.object.models.apartment import Apartment
from app.object.models.commercial import Commercial


def register_event_listeners():
    for model in [Land, Apartment, Commercial]:
        register_event_listener(model)
