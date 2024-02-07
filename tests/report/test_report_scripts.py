import pytest

from report_scripts import match_category, match_topics, get_sentiment


# def test_match_category():
#     product_data = ['保濕精華液', '粉底', '香水髮油']
#     matched_category = match_category(product_data)
#     # print(matched_category)
#     assert matched_category == [{'name': '保養'}, {'name': '美妝'}, {'name': '髮品'}]


def test_match_topic():
    review_data = ['出貨']
    matched_topic = match_topics(review_data)
    assert matched_topic[0]['name'] == '運送速度'


if __name__ == '__main__':
    pytest.main([__file__])
