from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from modelbase import ModelBase
from consts import dbpath

engine = create_engine(dbpath, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    import models
    ModelBase.metadata.create_all(bind=engine)

def get_db() -> Session: # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def stop_sessions():
    SessionLocal.close_all()
