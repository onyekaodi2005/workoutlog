from sqlmodel import SQLModel, create_engine
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./fitlog.db')
engine = create_engine(DATABASE_URL, echo=False)

async def init_db():
    SQLModel.metadata.create_all(engine)
