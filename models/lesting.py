from sqlmodel import SQLModel,Field
from datetime import date,datetime
from enum import Enum


class ListingTypes(str,Enum):
    service='שירות'
    equipment="ציוד"

class ListingStatus(str,Enum):
    active = "active"
    removed = "removed"

class Listing(SQLModel, table =True):
    __tablename__='Listing'
    id:int|None = Field(primary_key=True, default=None)
    userid : int
    categoryid:int
    type: ListingTypes
    status : ListingStatus = "active"
    title:str
    description:str
    imageFile:str | None = None
    price:int
    availability:str
    createdat:date =Field(default_factory=datetime.now)
    removedat:date 
    removedreason:str
