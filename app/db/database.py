from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(str(settings.database_url), echo=False)\

Session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
