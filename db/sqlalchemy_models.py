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


class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    products = relationship('Product', back_populates='brand')
    ecommerce = relationship('Ecommerce', back_populates='brands')
    brand_rating = relationship('BrandRating', back_populates='brand')

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship('Brand', back_populates='products')
    rating = relationship('Rating', back_populates='product')
    reviews = relationship('Reviews', back_populates='product')

class Ecommerce(Base):
    __tablename__ = 'ecommerce'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = relationship('Brand', back_populates='ecommerce')

class BrandRating(Base):
    __tablename__ = 'brand_rating'
    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship('Brand', back_populates='brand_rating')

class Rating(Base):
    __tablename__ = 'rating'
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Product', back_populates='rating')

class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Product', back_populates='comments')
    topics = Column(JSON)  # 將 topics 欄位的類型修改為 JSON
    sentiment_id = Column(Integer, ForeignKey('sentiment.id'))
    sentiment = relationship('Sentiment', back_populates='comments')

class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Sentiment(Base):
    __tablename__ = 'sentiment'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    reviews = relationship('Reviews', back_populates='sentiment')

class Month(Base):
    __tablename__ = 'month'
    id = Column(Integer, primary_key=True)
    brands = relationship('Brand', secondary='brand_month_association')
    products = relationship('Product', secondary='product_month_association')

# 中間表
brand_month_association = Table('brand_month_association', Base.metadata,
    Column('brand_id', Integer, ForeignKey('brand.id')),
    Column('month_id', Integer, ForeignKey('month.id'))
)

product_month_association = Table('product_month_association', Base.metadata,
    Column('product_id', Integer, ForeignKey('product.id')),
    Column('month_id', Integer, ForeignKey('month.id'))
)

comment_topic_association = Table('reviews_topic_association', Base.metadata,
    Column('reviews_id', Integer, ForeignKey('reviews.id')),
    Column('topic_id', Integer, ForeignKey('topic.id'))
)


engine = create_engine('sqlite:///:memory:') #創建數據庫引擎
Base.metadata.create_all(bind=engine) #建立資料庫中的資料表

# 使用 sessionmaker 創建一個 Session 來進行資料庫操作，像是conn
Session = sessionmaker(bind=engine)
session = Session()
