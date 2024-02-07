import settings
import requests
import json
import pandas as pd
from requests.exceptions import RequestException, JSONDecodeError

# category 標記
categories = settings.categories
def match_category(text):
    marked_categories = []
    for category_name, category_keywords in categories.items():
        for category_keyword in category_keywords:
            if category_keyword in text:
                marked_category = {
                    'name': category_name
                }
                marked_categories.append(category_name)
                break
    return marked_categories



# 維度標記
topics = settings.topics

def match_topics(text):
    matched_topics = []
    for topic_name, topic_keywords in topics.items():
        for topic_keyword in topic_keywords:
            if topic_keyword in text:
                matched_topic = {
                    'name': topic_name
                }
                matched_topics.append(matched_topic)
                break
    return matched_topics



# 情緒標記
api_key = settings.sentiment_api_key
api_url = settings.sentiment_api_url

def get_sentiment(doc_id, doc_content):
    responses = []
    headers = {
        'Content-Type': "application/json",
        'X-API-Key': api_key,
    }
    # API 請求參數
    payload = json.dumps({
        "dev_mode": False,
        "app_name": "Testing",
        "doc_list": [
            {
                "id": doc_id,
                "content": doc_content,
            }
        ]
    })

    session = requests.session()
    for doc in doc_content:
        response = session.post(api_url, headers=headers, data=payload)
    responses.append(json.loads(response.text))

    return responses


def find_matched_topic(row):
    matched_topics = []
    for topic in row['topic']:
        if row['category'] in topic:
            matched_topics.append(topic)
    return matched_topics


if __name__ == '__main__':
    data = {
        'ecommerce': ['momo', 'momo', 'momo', 'momo', 'momo', 'momo', 'shopee', 'shopee', 'shopee', 'shopee', 'shopee'],
        'brand': ['Lan', 'Lan', 'LRP', 'LRP', 'LRP', 'YSL', 'Lan', 'Lan', 'Lan', 'LOAP', 'LOAP'],
        'product': ['精華', '精華', '乳霜', '乳霜', '抗痘凝膠', '口紅', '粉底液', '粉底液', '粉底液', '乳霜', '乳液'],
        'reviews': ['服務很好', '服務很不好，價格也很貴', '服務很好，價格也很貴', '服務很不好，價格也很便宜', '服務', '價格', '價格', '品質', '服務包裝', '價格', '品質'],
        'category': ['髮品', '保養', '保養', '保養', '保養', '保養', '美妝', '美妝', '美妝', '保養', '髮品'],
        'topic': [['保養-服務', '美妝-品質'], ['保養-服務', '保養-價格', '美妝-品質'], ['保養-服務'], ['保養-價格'], ['保養-價格'], ['保養-保濕'], ['美妝-品質'], ['美妝-品質'], ['美妝-品質'], ['保養-保濕'], ['髮品-服務']],
    }
    df = pd.DataFrame(data)

    df['matched_topic'] = df.apply(find_matched_topic, axis=1)
    print(df)

'''
if __name__ == '__main__':
    doc = [
        "服務很好",
        "服務很不好",
        "價格很貴",
        "價格很便宜",
        "品質很差",
        "態度超不好",
        "服務",
    ]

    sentiment = map(lambda x: get_sentiment(x[0] + 1, x[1]), enumerate(doc))
    #只擷取 sentiment_tag 的值
    sentiment_tags = [result[0]['data'][0]['sentiment_tag']for result in sentiment]
    print(type(sentiment_tags))
'''
