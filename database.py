from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('db_username')}:{os.getenv('db_password')}"
    f"@{os.getenv('host_server')}:5432/{os.getenv('database_name')}?sslmode=require"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()