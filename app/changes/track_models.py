
from app.changes.funcs import register_event_listener

from app.metro.model import Metro
from app.auth.model import User
from app.object.models.land import Land
from app.object.models.apartment import Apartment
from app.object.models.commercial import Commercial
from app.district.model import District


def register_event_listeners():
    for model in [Land, Metro, User, Apartment, Commercial, District]:
        register_event_listener(model)
