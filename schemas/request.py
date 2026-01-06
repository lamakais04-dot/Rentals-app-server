from pydantic import BaseModel
from datetime import date
from enum import Enum

class Request(BaseModel):
    fromdate:date
    todate: date
    note:str | None =  None

class RequestUpdate(BaseModel):
    fromdate:date | None =  None
    todate: date | None =  None
    note:str | None =  None
