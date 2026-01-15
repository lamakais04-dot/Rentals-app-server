from fastapi import APIRouter,HTTPException,Depends
from sqlmodel import Session,select
from db import engine
from models.user import User
from auth_helper import get_user



router = APIRouter()

@router.get("/")
def getUsers(userId: int = Depends(get_user)):
    with Session(engine) as session:
        statement = select(User)
        response = session.exec(statement).all()
        return response    

@router.get("/{user_id}")
def getUser(user_id:int):
    with Session(engine) as session:
        user = session.get(User,user_id)
        if not user:
            raise HTTPException(status_code=404, detail="This user does not exist")
        return user  


    


