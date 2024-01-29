import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

DATABASE_URL = "sqlite:///./test_crud.db"


@pytest.fixture(scope="module")
def db_engine():
    return create_engine(DATABASE_URL)


@pytest.fixture(scope="module")
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    Base.metadata.create_all(bind=db_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
