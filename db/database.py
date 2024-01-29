from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base
from settings import database_url

engine = create_engine(database_url, echo=True)
Base.metadata.create_all(engine)


# get session with context management
def get_session():
    Session = sessionmaker(bind=engine)
    return Session()
