import pytest

from crud.review import create_review, get_review, update_review, delete_review, append_topic, remove_topic
from crud.topic import create_topic
from schemas.review import ReviewCreate, ReviewUpdate
from schemas.topic import TopicCreate


def test_create_review(db_session):
    review_data = ReviewCreate(text="Test Review", rating=4.5, product_id=1, post_time="2024-01-01 00:00:00")
    review = create_review(db_session, review_data)
    assert review.id is not None
    assert review.text == "Test Review"


def test_get_review(db_session):
    review_data = ReviewCreate(text="Test Review", rating=4.5, product_id=1, post_time="2024-01-01 00:00:00")
    review = create_review(db_session, review_data)
    retrieved_review = get_review(db_session, review.id)
    assert retrieved_review is not None
    assert retrieved_review.text == review.text


def test_update_review(db_session):
    review_data = ReviewCreate(text="Test Review", rating=4.5, product_id=1, post_time="2024-01-01 00:00:00")
    review = create_review(db_session, review_data)
    updated_data = ReviewUpdate(text="Updated Test Review", rating=5.0)
    updated_review = update_review(db_session, review.id, updated_data)
    assert updated_review is not None
    assert updated_review.text == "Updated Test Review"


def test_delete_review(db_session):
    review_data = ReviewCreate(text="Test Review", rating=4.5, product_id=1, post_time="2024-01-01 00:00:00")
    review = create_review(db_session, review_data)
    delete_review(db_session, review.id)
    deleted_review = get_review(db_session, review.id)
    assert deleted_review is None


def test_append_topic(db_session):
    review_data = ReviewCreate(text="Test Review", rating=4.5, product_id=1, post_time="2024-01-01 00:00:00")
    review = create_review(db_session, review_data)
    topic_data = TopicCreate(name="Quality")
    topic = create_topic(db_session, topic_data)
    updated_review = append_topic(db_session, review.id, topic.id)
    assert updated_review is not None
    assert updated_review.topics[0].name == "Quality"


def test_remove_topic(db_session):
    review_data = ReviewCreate(text="Test Review", rating=4.5, product_id=1, post_time="2024-01-01 00:00:00")
    review = create_review(db_session, review_data)
    topic_data_list = [
        TopicCreate(name="Quality"),
        TopicCreate(name="Price"),
        TopicCreate(name="Service")
    ]
    topic_list = [create_topic(db_session, topic_data) for topic_data in topic_data_list]
    for topic in topic_list:
        append_topic(db_session, review.id, topic.id)
    updated_review = remove_topic(db_session, review.id, topic_list[1].id)
    assert updated_review is not None
    assert len(updated_review.topics) == 2
    assert updated_review.topics[0].name == "Quality"


if __name__ == '__main__':
    pytest.main([__file__])
