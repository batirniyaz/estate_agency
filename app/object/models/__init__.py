from enum import Enum


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


class LocationCommercial(Enum):
    BUSINESS_CENTER = 'business_center'
    ADMINISTRATIVE_BUILDING = 'administrative_building'
    RESIDENTIAL_BUILDING = 'residential_building'
    COTTAGE = 'cottage'
    SHOPPING_MALL = 'shopping_mall'
    INDUSTRIAL_ZONE = 'industrial_zone'
    MARKET = 'market'
    DETACHED_BUILDING = 'detached_building'


class LocationLand(Enum):
    CITY = 'city'
    SUBURB = 'suburb'
    COUNTRYSIDE = 'countryside'
    ALONG_ROAD = 'along_road'
    NEAR_POND = 'near_pond'
    FOOTHILLS = 'foothills'
    COTTAGE_AREA = 'cottage_area'
    CLOSED_AREA = 'closed_area'


