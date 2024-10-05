from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.base import Base

database_file = r"../kondate.db"
# database_file = r"E:\Documents\SE\local\sqlite\db\kondate.db"

engine = create_engine("sqlite:///" + database_file, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
