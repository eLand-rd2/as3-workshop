import pytest

from report_scripts import match_category, match_topics, get_sentiment


def test_match_category():
    product_data = '香水髮油'
    matched_category = match_category(product_data)
    assert len(matched_category) > 0
    assert matched_category[0]['name'] == '髮品'
    assert matched_category[1]['name'] == '香水'


def test_match_topics():
    review_data = '快速出貨，包裝很完整'
    matched_topic = match_topics(review_data)
    assert len(matched_topic) > 0
    assert matched_topic[0]['name'] == '運送速度'
    assert matched_topic[1]['name'] == '包裝設計'

def test_match_topics_unmatched():
    review_data = '很讚'
    matched_topic = match_topics(review_data)
    assert len(matched_topic) == 0


def test_get_sentiment():
    review_data = '包裝的很爛，差評，不喜歡'
    sentiment = get_sentiment(1, review_data)
    assert len(sentiment) > 0
    assert sentiment == '負面'

if __name__ == '__main__':
    pytest.main([__file__])
