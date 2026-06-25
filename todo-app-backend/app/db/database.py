from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import get_settings
from app.models.base import Base

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, echo=True)

Sessionlocal = sessionmaker[Session](bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
        

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally: 
        db.close()
        
        
