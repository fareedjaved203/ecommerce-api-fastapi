from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..constants import DB_URL

if not DB_URL:
    raise ValueError("DB_URL environment variable is not set.")

engine = create_engine(DB_URL)

@event.listens_for(engine, "connect")
def connect_event_handler(dbapi_connection, connection_record):
    print("Database connected")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()