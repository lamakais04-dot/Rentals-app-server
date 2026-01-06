from pydantic import BaseModel
from enum import Enum

class ListingTypes(str,Enum):
    service='service'
    equipment='equipment'

class listing(BaseModel):
    userid:int
    title:str
    description:str
    price:int
    availability:str
    categoryid:int
    imageurl:str | None = None
    type:ListingTypes

class ListingUpdate(BaseModel):
    title:str | None = None
    description:str | None = None
    price:int | None = None
    availability:str | None = None
    categoryid:int | None = None
    imageurl:str | None = None
    type:ListingTypes | None = None
