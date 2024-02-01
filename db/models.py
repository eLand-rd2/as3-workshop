from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from . import Base


class Brand(Base):
    __tablename__ = 'brand'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    ecommerce: Mapped[str] = mapped_column(default=None)

    products: Mapped[List['Product']] = relationship('Product', back_populates='brand')


class Product(Base):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    rating: Mapped[float] = mapped_column(default=3.0)

    brand_id: Mapped[int] = mapped_column(ForeignKey('brand.id'))
    brand: Mapped['Brand'] = relationship('Brand', back_populates='products')
    reviews: Mapped[List['Review']] = relationship(back_populates='product')


class ReviewTopicAssociation(Base): # 用於建立reviews & topics 之間的多對多關係
    __tablename__ = 'review_topic_association'
    review_id = mapped_column(ForeignKey('reviews.id'), primary_key=True)
    topic_id = mapped_column(ForeignKey('topic.id'), primary_key=True)
    review: Mapped['Review'] = relationship(back_populates='topic_associations')
    topic: Mapped['Topic'] = relationship(back_populates='review_associations')


class Review(Base):
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    post_time: Mapped[datetime]
    rating: Mapped[float] = mapped_column(default=3.0)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    sentiment_id: Mapped[int] = mapped_column(ForeignKey("sentiment.id"))
    sentiment: Mapped['Sentiment'] = relationship('Sentiment', back_populates='reviews')

    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped['Product'] = relationship(back_populates='reviews')
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
    name: Mapped[str]

    reviews: Mapped[List['Review']] = relationship(
        secondary='review_topic_association',
        back_populates='topics'
    )

    review_associations: Mapped[List['ReviewTopicAssociation']] = relationship(
        'ReviewTopicAssociation',
        back_populates='topic'
    )

class Sentiment(Base):
    __tablename__ = 'sentiment'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))
    reviews: Mapped['Review'] = relationship('Review', back_populates='sentiment')

class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))
    reviews: Mapped['Review'] = relationship('Review', back_populates='category')