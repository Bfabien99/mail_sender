from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session
from typing import Annotated
from fastapi import Depends


engine = create_engine("sqlite:///maildb.db", echo=True)
SessionLocal = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Depends(get_db)
DBSession = Annotated[Session, SessionDep]