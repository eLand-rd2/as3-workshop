from sqlalchemy.orm import Session
from db.models import Topic
from schemas.topic import TopicCreate, TopicUpdate
from typing import Tuple



def create_topic(db: Session, topic: TopicCreate):
    db_topic = Topic(**topic.model_dump())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_topic(db: Session, topic_id: int) -> Tuple[Topic, int]:
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    return topic, topic.id if topic else None


def update_topic(db: Session, topic_id: int, topic: TopicUpdate):
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if db_topic:
        update_data = topic.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_topic, key, value)
        db.commit()
        db.refresh(db_topic)
        return db_topic
    return None


def delete_topic(db: Session, topic_id: int):
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if db_topic:
        db.delete(db_topic)
        db.commit()
    return {"msg": "Topic deleted"}
