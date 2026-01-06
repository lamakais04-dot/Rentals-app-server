from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session,select
from db import engine
from models.lesting import Listing
from schemas.lesting import listing


router = APIRouter()

@router.get("/")
def getLestings():
    with Session(engine) as session:
        statement = select(Listing)
        response = session.exec(statement).all()
        return response    

@router.post("/")
def createListing(listing_req: listing):
    with Session(engine) as session:
        listing_dict = listing_req.model_dump()
        listing = Listing(**listing_dict)
        session.add(listing)
        session.commit()
        session.refresh(listing)
        return listing