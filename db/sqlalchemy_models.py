# 使用 create_engine 函數建立到資料庫的連線

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship
# import auto now function
from sqlalchemy.sql import func

from db.database import Base


class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    products = relationship('Product', back_populates='brand')
    ecommerce = Column(String)
    # brand_rating = relationship('BrandRating', back_populates='brand')


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship('Brand', back_populates='products')
    rating = Column(Float, default=0.0)
    reviews = relationship('Reviews', back_populates='product')


class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    post_time = Column(DateTime)
    rating = Column(Float)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Product', back_populates='reviews')
    topics = relationship('Topic', secondary='reviews_topic_association')

    sentiment = Column(String, default='中立')
    created_at = Column(DateTime, default=func.now())


class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # keywords = Column(JSON)


# 中間表
brand_month_association = Table('brand_month_association', Base.metadata,
                                Column('brand_id', Integer, ForeignKey('brand.id')),
                                Column('month_id', Integer, ForeignKey('month.id'))
                                )

product_month_association = Table('product_month_association', Base.metadata,
                                  Column('product_id', Integer, ForeignKey('product.id')),
                                  Column('month_id', Integer, ForeignKey('month.id'))
                                  )

reviews_topic_association = Table('reviews_topic_association', Base.metadata,
                                  Column('reviews_id', Integer, ForeignKey('reviews.id')),
                                  Column('topic_id', Integer, ForeignKey('topic.id'))
                                  )
