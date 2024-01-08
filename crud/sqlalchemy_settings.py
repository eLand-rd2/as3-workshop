import json
# 使用 create_engine 函數建立到資料庫的連線
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 資料庫
engine = create_engine('sqlite:///AS3_data.db')

# 使用 declarative_base 創建一個基礎類別，並定義資料表的模型
Base = declarative_base()


class EcommerceReviews(Base):
    __tablename__ = 'ecommerce_reviews'

    id = Column(Integer, primary_key=True)
    brand = Column(String)  # 品牌名
    source = Column(String)  # 電商來源
    product = Column(String)  # 產品名稱
    common = Column(String)  # 評論內容
    rating = Column(Float)  # 產品星等
    month = Column(Integer)  # 評論留言的發表月份


class ReviewsCategory(Base):
    __tablename__ = 'reviews_category'

    id = Column(Integer, primary_key=True)
    brand = Column(String)   # 品牌名
    source = Column(String)  # 電商來源
    product = Column(String)  # 產品名稱
    common = Column(String)  # 評論內容
    sent = Column(String)  # 評論的情緒
    month = Column(Integer)  # 評論留言的發表月份
    topic = Column(JSON)  # 評論內容命中的話題維度分類

    # 因為資料表的維度是用list儲存，資料庫內的Col不能用list格式儲存 所以先將其轉換成JSON格式再儲存，JSON會比str通用
    def set_topic(self, topic):  # set_topic 是用於資料庫存儲前的轉換
        # 如果 topic 不是字串，則將其轉換為 JSON 字串
        if not isinstance(topic, str):
            self.topic = json.dumps(topic)
        else:
            self.topic = topic

    def get_topic(self):  # get_topic 是用於資料庫讀取時的轉換
        # 將 JSON 字串解析回列表
        return json.loads(self.topic)


# 使用 Base.metadata.create_all(bind=engine) 來建立資料庫中的資料表
Base.metadata.create_all(bind=engine)

# 使用 sessionmaker 創建一個 Session 來進行資料庫操作，像是conn
Session = sessionmaker(bind=engine)
session = Session()
