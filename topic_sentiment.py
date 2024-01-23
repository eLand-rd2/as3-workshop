import settings
from report_scripts import match_topics, get_sentiment
import pandas as pd
from datetime import datetime
import dateutil.relativedelta

# 呼叫並連接資料庫
df = {}


# 拉出上個月的rawdata
now = datetime.now()  # 取得當前日期和時間
last_month = now+dateutil.relativedelta.relativedelta(months=-1)  # 取的上個月的日期
last_month = last_month.month
df = df[df['month'] == last_month]  # 取得上個月的資料


# 進行維度標記，並儲存回去資料庫
df['matched_topics'] = df['reviews'].apply(match_topics)  # 維度標記
# 儲存回資料庫



# 進行情緒標記，並儲存回去資料
docs = df['reviews']
sentiment = map(lambda x: get_sentiment(x[0] + 1, x[1]), enumerate(docs))  # 情緒標記
#只擷取 sentiment_tag 的值
sentiment_tags = [result[0]['data'][0]['sentiment_tag']for result in sentiment]
sentiment_tags_series = pd.Series(sentiment_tags, name='sentiment_tag')
df = pd.concat([df, sentiment_tags_series], axis=1)
# 儲存回資料庫
