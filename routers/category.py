from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session,select
from db import engine
from models.category import Category
from schemas.category import category

router = APIRouter()

@router.get("/")
def getCategories():
    with Session(engine) as session:
        statement = select(Category)
        response = session.exec(statement).all()
        return response    

@router.post("/")
def createCategory(category_req: category):
    with Session(engine) as session:
        category_dict = category_req.model_dump()
        category = Category(**category_dict)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category