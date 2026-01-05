from sqlmodel import create_engine


DATABASE_URL="postgresql://postgres:1504@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
