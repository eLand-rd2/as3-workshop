import settings
import requests
import json
from requests.exceptions import RequestException, JSONDecodeError



# 維度標記
topics = settings.topics

def match_topics(text):
    matched_topics = []
    for topic_name, keywords in topics.items():
        for keyword in keywords:
            if keyword in text:
                matched_topics.append(topic_name)
                break
    return matched_topics



# 情緒標記
api_key = settings.sentiment_api_key
api_url = settings.sentiment_api_url
def get_sentiment(doc):
    headers = {
        'Content-Type': "application/json",
    }
    # API 請求參數
    payload = json.dumps({
        "dev_mode": False,
        "app_name": "Testing",
        "doc_list": []
    })

    session = requests.session()
    for doc in docs:
        response = session.post(api_url, headers=headers, data=payload)
    print(response.text)

if __name__ == '__main__':
    docs = [
        "服務很好，價格也很便宜",
        "服務很不好，價格也很貴",
        "服務很好，價格也很貴",
        "服務很不好，價格也很便宜",
    ]
    sentiment = map(get_sentiment, docs)
    print(list(sentiment))


# 計算 P/N 比
def PN_ratio(positive, negative):
    if negative == 0:
        pn = '-'
    elif negative != 0 and positive == 0:
        pn = 0
    else:
        pn = round(positive / negative, 2)
    return



