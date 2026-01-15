from sqlmodel import SQLModel,Field
from datetime import date
from enum import Enum

class UserGender(Enum):
    male = "male"
    female = "female"
    other = "other"

class User(SQLModel,table = True):
    __tablename__ = 'User'
    id: int|None = Field(primary_key=True , default=None)
    firstname: str
    lastname: str
    birthdate: date
    address: str
    gender: UserGender
    email:str = Field(unique=True)
    hashedpassword:str
    phonenumber:str = Field(unique=True)
    isadmin:bool = False
    imageurl:str | None = None

 