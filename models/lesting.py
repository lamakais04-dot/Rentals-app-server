from sqlmodel import SQLModel,Field
from datetime import date
from enum import Enum
from typing import Annotated

class ListingTypes(str,Enum):
    service='service'
    equipment="equipment"

class ListingStatus(str,Enum):
    active = "active"
    removed = "removed"

class Listing(SQLModel, table =True):
    __tablename__='Listing'
    id:int|None = Field(primary_key=True, default=None)
    userid : int
    categoryid:int
    type: ListingTypes
    status : ListingStatus
    title:str
    description:str
    imageurl:str | None = None
    price:int
    availability:str
    createdat:date
    removedat:date
    removedreason:str
