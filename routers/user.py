from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session,select
from db import engine
from models.user import User

router = APIRouter()

@router.get("/")
def getUsers():
    with Session(engine) as session:
        statement = select(User)
        response = session.exec(statement).all()
        return response    

