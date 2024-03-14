import pytest

from report_scripts import match_category, match_topics, get_sentiment


# def test_match_category():
#     product_data = '香水髮油'
#     matched_category = match_category(product_data)
#     assert len(matched_category) > 0
#     assert matched_category[0]['name'] == '髮品'
#     assert matched_category[1]['name'] == '香水'


def test_match_topics():
    review_data = '包裝完整，寄貨速度快'
    matched_topic = match_topics(review_data)
    print(matched_topic)
    assert len(matched_topic) > 0
    # assert matched_topic[0]['name'] == ['Package', 'Efficacy']
    # assert matched_topic[1]['name'] == 'Package'

# def test_match_topics_unmatched():
#     review_data = '很讚'
#     matched_topic = match_topics(review_data)
#     assert len(matched_topic) == 0


# def test_get_sentiment():
#     review_data = '出貨速度快，產品效期長，贈品精緻不粗糙，價格優惠，很讚'
#     sentiment = get_sentiment(1, review_data)
#     assert len(sentiment) > 0
#     assert sentiment == '負面'

if __name__ == '__main__':
    pytest.main([__file__])
