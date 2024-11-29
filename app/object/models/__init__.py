from sqlalchemy import Enum


class ActionType(Enum):
    RENT = 'rent'
    SALE = 'sale'


class Category(Enum):
    APARTMENT = 'apartment'
    LAND = 'land'
    COMMERCIAL = 'commercial'


class HouseType(Enum):
    NEW_BUILDING = 'new_building'
    SECONDARY = 'secondary'


class BathroomType(Enum):
    SEPERATED = 'seperated'
    COMBINED = 'combined'
    MANY = 'many'


class HouseCondition(Enum):
    EURO = 'euro'
    NORMAL = 'normal'
    REPAIR = 'repair'
