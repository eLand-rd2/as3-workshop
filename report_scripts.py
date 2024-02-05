import settings
import requests
import json
from requests.exceptions import RequestException, JSONDecodeError

# category 標記
categories = settings.categories
def mark_category(text):
    marked_categories = []
    for category_name, category_keywords in categories.items():
        for category_keyword in category_keywords:
            if category_keyword in text:
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

'''
if __name__ == '__main__':
    docs = [
        "服務很好",
        "服務很不好",
        "價格很貴",
        "價格很便宜",
        "品質很差",
        "態度超不好",
        "服務",
    ]
    sentiment = map(lambda x: get_sentiment(x[0] + 1, x[1]), enumerate(docs))
    #只擷取 sentiment_tag 的值
    sentiment_tags = [result[0]['data'][0]['sentiment_tag']for result in sentiment]
    print(sentiment_tags)
'''


