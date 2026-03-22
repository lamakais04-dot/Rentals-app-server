from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from sqlmodel import Session, select
from auth_helper import get_user
from db import engine
from models.category import Category
from models.lesting import Listing
from schemas.category import category
router = APIRouter()


@router.get("/")
def getCategories():
    with Session(engine) as session:
        statement = select(Category)
        response = session.exec(statement).all()
        return response


@router.get("/{category_id}")
def get_category_name(category_id: int):
    with Session(engine) as session:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="This category does not exist")
        return category


@router.post("/")
def createCategory(category_req: category, userObj=Depends(get_user)):
    if not userObj["isAdmin"]:
        return
    with Session(engine) as session:
        category_dict = category_req.model_dump()
        category = Category(**category_dict)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category


@router.get("/my/categories")
def get_my_categories(userObj=Depends(get_user)):
    with Session(engine) as session:
        userId = userObj["id"]
        stmt = (
            select(Category.id, Category.name)
            .join(Listing, Listing.categoryid == Category.id)
            .where(Listing.userid == userId)
            .distinct()
        )
        categories = session.exec(stmt).all()

        return [{"id": c.id, "name": c.name} for c in categories]
    
@router.put("/{id}")
def update_listing(
    id: int, category_update:category , user = Depends(get_user)
):
    with Session(engine) as session:
        categoryUpdate_dict = category_update.model_dump(exclude_none=True)
        print(categoryUpdate_dict)
        category = session.get(Category, id)
        print(category.model_dump())
        if not category:
            raise HTTPException(status_code=404, detail="This listing does not exist")
        for key, value in categoryUpdate_dict.items():
            setattr(category, key, value)
        session.commit()
        session.refresh(category)
        return category.model_dump()


@router.delete("/delete/{category_id}")
def delete_category_by_admin(category_id: int, userObj=Depends(get_user)):
    if not userObj["isAdmin"]:
        return
    with Session(engine) as session:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="This listing does not exist")
        session.delete(category)
        session.commit()
        return Response(status_code=204)
