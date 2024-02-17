from sqlalchemy.orm import Session

from db.models import Review, Topic, ReviewTopicAssociation

from schemas.review import ReviewCreate, ReviewUpdate, ReviewBase
from schemas.topic import TopicCreate

def create_review(db: Session, review: ReviewCreate): # 這個是給廣興用來存進去的
    db_review = Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def create_or_get_review(db: Session, product_id, review_text, review_post_time, review_rating, review_sentiment, review_order_id):
    existing_review = db.query(Review).filter(Review.order_id == review_order_id).first()
    if existing_review:
        # print("品牌名稱：" + str(product_data.name) + "id:" +  int(existing_product.id))
        return existing_review
    else:
        review_data = ReviewCreate(text = review_text,
                            post_time = review_post_time,
                            rating = review_rating,
                            sentiment = review_sentiment,
                            order_id = review_order_id,
                            product_id = product_id)
        new_review = Review(**review_data.dict())
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review

def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews(db: Session, begin, end, order_by='post_time', limit=100, offset=0):
    query_result = db.query(Review).filter(Review.post_time >= begin).filter(Review.post_time <= end).order_by(order_by).limit(limit).offset(offset).all()
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


def append_topic(db: Session, review_id, topic_id): # Serena更新topic用
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
