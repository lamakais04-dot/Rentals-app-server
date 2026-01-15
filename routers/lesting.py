from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Query, Cookie
from fastapi.responses import JSONResponse, Response
from sqlmodel import Session, select
from db import engine
from typing import Optional, List
from models.lesting import Listing
from models.user import User
from schemas.lesting import listing, ListingUpdate
import boto3
import uuid
from auth_helper import get_user


router = APIRouter()
# userId:int = Depends(get_user)


@router.get("/")
def getLestings():
    with Session(engine) as session:
        statement = select(Listing)
        response = session.exec(statement).all()
        return response


@router.get("/user")
def getListingsWithTheUserData(
    page: int = Query(default=1),
    page_size: int = Query(default=6),
    categories: Optional[List[int]] = Query(default=None),
):
    offset = (page - 1) * page_size
    with Session(engine) as session:
        statement = select(Listing, User).join(User, User.id == Listing.userid)
        if categories:
            statement = statement.where(Listing.categoryid.in_(categories))
        statement = statement.offset(offset=offset).limit(page_size)
        result = session.exec(statement).all()
        return [
            {
                **listing.model_dump(),
                "user": {"address": user.address, "name": user.firstname},
            }
            for listing, user in result
        ]


@router.get("/withoutMine")
def getListingsWithoutMine(
    userId: int = Depends(get_user),
    page: int = Query(default=1),
    page_size: int = Query(default=6),
    categories: Optional[List[int]] = Query(default=None),
):
    offset = (page - 1) * page_size
    with Session(engine) as session:
        statement = (
            select(Listing, User)
            .join(User, User.id == Listing.userid)
            .where(userId != Listing.userid)
        )
        if categories:
            statement = statement.where(Listing.categoryid.in_(categories))
        statement = statement.offset(offset=offset).limit(page_size)
        result = session.exec(statement).all()
        return [
            {
                **listing.model_dump(),
                "user": {"address": user.address, "name": user.firstname},
            }
            for listing, user in result
        ]


@router.get("/get/my")
def get_my_listings(
    userId: int = Depends(get_user),
    categoryId: int | None = None,
):
    with Session(engine) as session:
        statement = select(Listing).where(Listing.userid == userId)
        if categoryId:
            statement = statement.where(Listing.categoryid == categoryId)
        res = session.exec(statement).all()
        return res


@router.get("/{listing_id}")
def getLestingsById(listing_id: int):
    with Session(engine) as session:
        listing = session.get(Listing, listing_id)
        if not listing:
            raise HTTPException(status_code=404, detail="This listing does not exist")
        return listing


@router.post("/")
def createListing(listing_req: listing, userId: int = Depends(get_user)):
    with Session(engine) as session:
        listing_dict = listing_req.model_dump()
        print(listing_dict)
        listing = Listing(**listing_dict)
        session.add(listing)
        session.commit()
        session.refresh(listing)
        return listing


@router.post("/uploadImage")
def uploadImage(image_file: UploadFile = File()):
    s3_client = boto3.client("s3")
    splited_name_file = image_file.filename.split(".")
    file_extinsion = splited_name_file[len(splited_name_file) - 1]
    new_file_name = f"public/listings/{uuid.uuid4()}.{file_extinsion}"
    s3_client.upload_fileobj(
        image_file.file,
        "rentals-project-images-storage",
        new_file_name,
        ExtraArgs={"ContentType": file_extinsion},
    )
    url = f"https://rentals-project-images-storage.s3.eu-north-1.amazonaws.com/{new_file_name}"
    return url


@router.put("/{id}")
def update_listing(
    id: int, listingUpdate: ListingUpdate, userId: int = Depends(get_user)
):
    with Session(engine) as session:
        listingUpdate_dict = listingUpdate.model_dump(exclude_none=True)
        print(listingUpdate_dict)
        listing = session.get(Listing, id)
        print(listing.model_dump())
        if not listing:
            raise HTTPException(status_code=404, detail="This listing does not exist")
        for key, value in listingUpdate_dict.items():
            setattr(listing, key, value)
        session.commit()
        session.refresh(listing)
        return listing.model_dump()


@router.delete("/{id}")
def delete_listing(id: int, userId: int = Depends(get_user)):
    with Session(engine) as session:
        listing_to_delete = session.get(Listing, id)
        if not listing_to_delete:
            raise HTTPException(status_code=404, detail="This listing does not exist")
        session.delete(listing_to_delete)
        session.commit()
        return Response(status_code=204)
