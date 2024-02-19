from sqlalchemy.orm import Session, contains_eager
from db.models import Sentiment, Review
from schemas.sentiment import SentimentCreate, SentimentUpdate

def create_sentiment(db: Session, sentiment: SentimentCreate):
    db_sentiment = Sentiment(**sentiment.model_dump())
    db.add(db_sentiment)
    db.commit()
    db.refresh(db_sentiment)
    return db_sentiment


def get_sentiment(db: Session, sentiment_id: int):
    return db.query(Sentiment).filter(Sentiment.id == sentiment_id).first()

def get_sentiment_name(db: Session, sentiment_name: str):
    return db.query(Sentiment).filter(Sentiment.name == sentiment_name).first()

def update_sentiment_with_review(db: Session, reviews_id, sentiment: SentimentUpdate):
    # 從資料庫中取得特定ID的review
    review = db.query(Review).filter(Review.id == reviews_id).first()

    if review:
        # 更新review的情感
        review.sentiment = sentiment.name
        db.commit()
        db.refresh(review)
        return review
    return None


def delete_sentiment(db: Session, sentiment_id: int):
    db_sentiment = db.query(Sentiment).filter(Sentiment.id == sentiment_id).first()
    if db_sentiment:
        db.delete(db_sentiment)
        db.commit()
    return {"msg": "Sentiment deleted"}

