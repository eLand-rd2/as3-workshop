from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///:memory:')  # 創建數據庫引擎
Base.metadata.create_all(bind=engine)  # 建立資料庫中的資料表


# get session with context management
def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == '__main__':
    # test get_session
    with get_session() as sess:
        print(sess)
        print(type(sess))
