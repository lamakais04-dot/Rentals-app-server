import os

from dotenv import load_dotenv
from sqlmodel import create_engine

load_dotenv()

DEFAULT_DATABASE_URL = "postgresql://postgres:1504@localhost:5432/postgres"
DATABASE_URL = os.getenv("DATABASE_URL") or DEFAULT_DATABASE_URL
engine = create_engine(DATABASE_URL)
