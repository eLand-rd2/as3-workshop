import settings
from report_scripts import match_topics, get_sentiment
import pandas as pd

# 呼叫並連接資料庫

# 拉出還沒進行維度標記和情緒標記的rawdata

# 進行維度標記，並儲存回去資料庫
df['matched_topics'] = df['comment'].apply(match_topics)  # 維度標記
# 維度標記轉為二進制
topics = settings.topics
for topic in topics:
    df[topic] = df['matched_topics'].apply(lambda x: 1 if topic in x else 0)
# 儲存回資料庫



# 進行情緒標記，並儲存回去資料
docs = df['comment']
sentiment = map(lambda x: get_sentiment(x[0] + 1, x[1]), enumerate(docs))  # 情緒標記

#只擷取 sentiment_tag 的值
sentiment_tags = [result[0]['data'][0]['sentiment_tag']for result in sentiment]
sentiment_tags_series = pd.Series(sentiment_tags, name='sentiment_tag')
df = pd.concat([df, sentiment_tags_series], axis=1)

# 拆解 sentiment 欄位成 positve, negative, neutral三個欄位
sentiment_dummies = pd.get_dummies(df['sentiment_tag'], prefix='sentiment', dtype=int)
df = pd.concat([df, sentiment_dummies], axis=1)

# 儲存回資料庫
