from sqlalchemy.orm import Session

from db.models import Review, Topic
from schemas.review import ReviewCreate, ReviewUpdate


def create_review(db: Session, review: ReviewCreate):
    db_review = Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews(db: Session, begin, end, order_by='post_time', limit=100, offset=0):
    query_result = db.query(Review).filter(Review.post_time >= begin).filter(Review.post_time < end).order_by(order_by).limit(limit).offset(offset).all()
    return query_result

def update_review(db: Session, review_id: int, review: ReviewUpdate):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        update_data = review.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
        return db_review
    return None


def delete_review(db: Session, review_id: int):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
    return {"msg": "Review deleted"}


def append_topic(db: Session, review_id, topic_id):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()

    if db_review and db_topic:
        db_review.topics.append(db_topic)
        db.commit()
        db.refresh(db_review)
        return db_review
    return None


def remove_topic(db: Session, review_id: int, topic_id: int):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()

    if db_review and db_topic:
        db_review.topics.remove(db_topic)
        db.commit()
        db.refresh(db_review)
        return db_review
