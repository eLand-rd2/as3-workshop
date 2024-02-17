from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, func, DateTime, String, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column

from . import Base

import pytz

# 获取亚洲/台北时区
taipei_timezone = pytz.timezone('Asia/Taipei')

# 定义默认值函数
def default_created_at():
    # 获取当前时间并转换为亚洲/台北时区
    current_time_taipei = datetime.now(taipei_timezone)
    return current_time_taipei


class Brand(Base):
    __tablename__ = 'brand'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    ecommerce: Mapped[str] = mapped_column(String(50), default=None)
    shop_id: Mapped[str] = mapped_column(String(20), default=None) #default=None 接受資料有空值

    products: Mapped[List['Product']] = relationship('Product', back_populates='brand')


class Product(Base):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    rating: Mapped[float] = mapped_column(Float, default=3.0)
    item_id: Mapped[str] = mapped_column(String(20), default=None)

    brand_id: Mapped[int] = mapped_column(ForeignKey('brand.id'))
    brand: Mapped['Brand'] = relationship('Brand', back_populates='products')

    reviews: Mapped[List['Review']] = relationship(back_populates='product')

    categories: Mapped[List['Category']] = relationship(
        secondary='product_category_association',
        back_populates='products'
    )
    category_associations: Mapped[List['ProductCategoryAssociation']] = relationship(
        'ProductCategoryAssociation',
        back_populates='product'
    )



class ReviewTopicAssociation(Base): # 用於建立reviews & topics 之間的多對多關係
    __tablename__ = 'review_topic_association'
    review_id = mapped_column(ForeignKey('reviews.id'), primary_key=True)
    topic_id = mapped_column(ForeignKey('topic.id'), primary_key=True)
    review: Mapped['Review'] = relationship(back_populates='topic_associations')
    topic: Mapped['Topic'] = relationship(back_populates='review_associations')


class Review(Base):
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(500))
    post_time: Mapped[datetime]
    rating: Mapped[float] = mapped_column(Float, default=3.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=default_created_at)
    sentiment: Mapped[str] = mapped_column(String(5))
    order_id: Mapped[str] = mapped_column(String(20), default=None)

    # sentiment_id: Mapped[int] = mapped_column(ForeignKey("sentiment.id"))
    # sentiment: Mapped['Sentiment'] = relationship('Sentiment', back_populates='reviews')

    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped['Product'] = relationship(back_populates='reviews')
    # 在reviews這個資料表內，有一欄叫做product，把這個資料表跟Product關聯起來，並透過back_populates指定是跟Product裡面的reviews做關聯

    topics: Mapped[List['Topic']] = relationship(
        secondary='review_topic_association',
        back_populates='reviews'
    )
    topic_associations: Mapped[List['ReviewTopicAssociation']] = relationship(
        'ReviewTopicAssociation',
        back_populates='review'
    )


class Topic(Base):
    __tablename__ = 'topic'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    reviews: Mapped[List['Review']] = relationship(
        secondary='review_topic_association',
        back_populates='topics'
    )

    review_associations: Mapped[List['ReviewTopicAssociation']] = relationship(
        'ReviewTopicAssociation',
        back_populates='topic'
    )

# class Sentiment(Base):
#     __tablename__ = 'sentiment'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#
#     review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))
#     reviews: Mapped['Review'] = relationship('Review', back_populates='sentiment')

class ProductCategoryAssociation(Base):  # 用於建立products & categories 之間的多對多關係
    __tablename__ = 'product_category_association'
    product_id = mapped_column(ForeignKey('product.id'), primary_key=True)
    category_id = mapped_column(ForeignKey('categories.id'), primary_key=True)
    product: Mapped['Product'] = relationship(back_populates='category_associations')
    category: Mapped['Category'] = relationship(back_populates='product_associations')


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), default=None)

    products: Mapped[List['Product']] = relationship(
        secondary='product_category_association',
        back_populates='categories'
    )

    product_associations: Mapped[List['ProductCategoryAssociation']] = relationship(
        'ProductCategoryAssociation',
        back_populates='category'
    )