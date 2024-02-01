from db.database import get_session
from report_scripts import match_topics, get_sentiment
import pandas as pd
from datetime import datetime
import dateutil.relativedelta
from schemas.topic import TopicCreate
from crud.topic import create_topic
from schemas.review import ReviewUpdate
from crud.review import update_review, get_reviews


'''
data = {
    'ecommerce': ['momo', 'momo', 'momo', 'momo', 'momo', 'momo', 'shopee', 'shopee', 'shopee', 'shopee', 'shopee'],
    'brand': ['Lan', 'Lan', 'LRP', 'LRP', 'LRP', 'Cerave', 'Lan', 'Lan', 'Lan', 'LOAP', 'LOAP'],
    'product': ['小黑瓶', '小黑瓶', '萬能霜', '萬能霜', '抗痘凝膠', 'PM乳', '小黑瓶', '零粉感', '零粉感', '紫熨斗', '紫熨斗'],
    'reviews': ['服務很好，價格也很便宜', '服務很不好，價格也很貴', '服務很好，價格也很貴', '服務很不好，價格也很便宜', '服務', '價格', '價格', '品質', '服務包裝', '價格', '品質'],
    'rating': [3, 5, 2, 3, 4, 5, 5, 4, 3, 5, 1],
    'month': [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]
}
df = pd.DataFrame(data)

# 拉出上個月的rawdata
now = datetime.now()  # 取得當前日期和時間
last_month = now+dateutil.relativedelta.relativedelta(months=-1)  # 取的上個月的日期
last_month = last_month.month
df = df[df['month'] == last_month]  # 取得上個月的資料
'''

# begin/end
# cli_scripts
# process sentiment/ process topic
# 平移、結束

# 呼叫並連接資料庫
# 篩選月份
def process_reviews(begin, end):
    now = datetime.now()  # 取得當前日期和時間
    last_month = now+dateutil.relativedelta.relativedelta(months=-1)  # 取的上個月的日期
    last_year = last_month.year
    last_month = last_month.month
    # 建立db連線
    session = get_session()
    try:
        # 使用 SQLAlchemy 篩選器擷取符合條件(上個月)的資料
        query_result = get_reviews(session, begin=begin, end=end, limit=limit, offset=offset)
        process_sentiment(query_result)
        process_topic(query_result)
        # 將查詢結果轉換為 Pandas DataFrame
    except Exception as e:
        print(f"Error fetching data from database: {str(e)}")

    finally:
        session.close()  # 關閉會話

def process_sentiment(reviews):
    # df = pd.read_sql(reviews.statement, session.bind)
    #
    # # 進行維度標記
    # df['topic'] = df['reviews'].apply(match_topics)
    #
    # # 進行情緒標記
    # docs = df['reviews']
    # sentiment_all = map(lambda x: get_sentiment(x[0] + 1, x[1]), enumerate(docs))
    # #只擷取 sentiment_tag 的值
    # sentiment = [result[0]['data'][0]['sentiment_tag']for result in sentiment_all]
    # sentiment_series = pd.Series(sentiment, name='sentiment')
    # df = pd.concat([df, sentiment_series], axis=1)


    # 儲存回資料庫
    # 使用 update_review 更新情緒標記
    update_data = ReviewUpdate(sentiment=df['sentiment'])
    update_review = update_review(session, df=['review_id'], update_data)
    # 使用 create_topic 創建維度標記
    topic_data = TopicCreate(name=df['topic'])
    topic = create_topic(session, topic_data)

def process_topic(reviews):
    pass
