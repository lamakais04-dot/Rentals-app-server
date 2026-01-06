from sqlmodel import SQLModel,Field


class Category(SQLModel,table = True):
    __tablename__='Category'
    id: int|None = Field(primary_key=True, default=None)
    name: str
 