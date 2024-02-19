import settings
import requests
import json
import pandas as pd
import re
from requests.exceptions import RequestException, JSONDecodeError

# category 標記
categories = settings.categories
def match_category(text):
    marked_categories = []
    for category_name, category_keywords in categories.items():
        for category_keyword in category_keywords:
            pattern = category_keyword
            if re.search(pattern, text):
                marked_category = {'name': category_name}
                marked_categories.append(marked_category)
                break
    return marked_categories



# 維度標記
topics = settings.topics

def match_topics(text):
    matched_topics = []
    for topic_name, topic_keywords in topics.items():
        for topic_keyword in topic_keywords:
            pattern = topic_keyword
            if re.search(pattern, text):
                matched_topic = topic_name
                # matched_topic = {'name': topic_name}
                # print('匹配成功')
                matched_topics.append(matched_topic)
                break
    return matched_topics



# 情緒標記
api_key = settings.sentiment_api_key
api_url = settings.sentiment_api_url

def get_sentiment(doc_id, doc_content):
    # responses = []
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
    # for doc in doc_content:
    response = session.post(api_url, headers=headers, data=payload)
    responses = json.loads(response.text)
    # print(responses)
    sentiment_tags = responses['data'][0]['sentiment_tag']
    return sentiment_tags


def find_matched_topic(row):
    matched_topics = []
    for topic in row['topic']:
        if row['category'] in topic:
            matched_topics.append(topic)
    return matched_topics

'''
if __name__ == '__main__':
    data = {
        'ecommerce': ['momo', 'momo', 'momo', 'momo', 'momo', 'momo', 'shopee', 'shopee', 'shopee', 'shopee', 'shopee'],
        'brand': ['Lan', 'Lan', 'LRP', 'LRP', 'LRP', 'YSL', 'Lan', 'Lan', 'Lan', 'LOAP', 'LOAP'],
        'product': ['精華', '精華', '乳霜', '乳霜', '抗痘凝膠', '口紅', '粉底液', '粉底液', '粉底液', '乳霜', '香水髮油'],
        'reviews': ['服務很好', '包裝很不好，而且價格也很貴', '服務很好，價格也很貴', '服務很不好，價格也很便宜', '服務', '價格', '價格', '品質', '服務包裝', '價格', '品質'],
    }
    df = pd.DataFrame(data)

    # df['match_category'] = df['product'].apply(match_category)
    df['match_topic'] = df['reviews'].apply(match_topics)
    print(df)

'''
if __name__ == '__main__':
    doc = ""
    sentiment = get_sentiment(1, doc)
    print(sentiment)

