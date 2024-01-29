import pytest

from crud.topic import create_topic, get_topic, update_topic, delete_topic
from schemas.topic import TopicCreate, TopicUpdate


def test_create_topic(db_session):
    topic_data = TopicCreate(name="Test Topic")
    topic = create_topic(db_session, topic_data)
    assert topic.id is not None
    assert topic.name == "Test Topic"


def test_get_topic(db_session):
    topic_data = TopicCreate(name="Test Topic")
    topic = create_topic(db_session, topic_data)
    retrieved_topic = get_topic(db_session, topic.id)
    assert retrieved_topic is not None
    assert retrieved_topic.name == topic.name


def test_update_topic(db_session):
    topic_data = TopicCreate(name="Test Topic")
    topic = create_topic(db_session, topic_data)
    updated_data = TopicUpdate(name="Updated Test Topic")
    updated_topic = update_topic(db_session, topic.id, updated_data)
    assert updated_topic is not None
    assert updated_topic.name == "Updated Test Topic"


def test_delete_topic(db_session):
    topic_data = TopicCreate(name="Test Topic")
    topic = create_topic(db_session, topic_data)
    delete_topic(db_session, topic.id)
    deleted_topic = get_topic(db_session, topic.id)
    assert deleted_topic is None


if __name__ == '__main__':
    pytest.main([__file__])
