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


def update_sentiment_with_review(db: Session, reviews_id: int, sentiment: SentimentUpdate):
    # 查詢與指定評論相關聯的sentiments
    db_sentiments = db.query(Sentiment).\
        join(Review).\
        filter(Review.id == reviews_id).\
        options(contains_eager(Sentiment.reviews)).\
        all()

    if db_sentiments:
        # 更新每個找到的sentiments
        for db_sentiment in db_sentiments:
            update_data = sentiment.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_sentiment, key, value)
        db.commit()
        return db_sentiments
    return None


def delete_sentiment(db: Session, sentiment_id: int):
    db_sentiment = db.query(Sentiment).filter(Sentiment.id == sentiment_id).first()
    if db_sentiment:
        db.delete(db_sentiment)
        db.commit()
    return {"msg": "Sentiment deleted"}

