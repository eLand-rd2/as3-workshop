from db.database import get_session
from report_scripts import match_topics, get_sentiment, match_category
import pandas as pd
from datetime import datetime, date
import dateutil.relativedelta
from schemas.topic import TopicCreate
from crud.topic import create_topic, get_topic_name
from crud.review import get_reviews, append_topic, update_review
from crud.product import get_products, append_category
from crud.category import create_category, get_category_name
from schemas.category import CategoryCreate
from crud.sentiment import create_sentiment, get_sentiment_name
from schemas.sentiment import SentimentCreate
import click


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



@click.command()
def process_reviews(begin, end, page_size=100):

    # 建立db連線
    session = get_session()
    try:
        offset = 0
        while True:
            # 使用 SQLAlchemy 篩選器擷取符合條件(上個月)的資料
            query_result = get_reviews(session, begin=begin, end=end, limit=page_size, offset=offset)

            if not query_result:
                break  # 沒有更多資料時

            process_sentiment(query_result)
            process_topic(query_result)

            # 更新 offset
            offset += page_size

            # 若處理完畢所有資料，跳出迴圈
            if len(query_result) < page_size:
                break

    except Exception as e:
        print(f"Error fetching data from database: {str(e)}")

    finally:
        session.close()  # 關閉會話

# @click.command()
# def process_products(page_size=100):
#     # 建立db連線
#     session = get_session()
#     try:
#         offset = 0
#         while True:
#             # 使用 SQLAlchemy 篩選器擷取符合條件(上個月)的資料
#             query_result = get_products(session, limit=page_size, offset=offset)
#
#             if not query_result:
#                 break  # 沒有更多資料時
#
#             process_category(query_result)
#
#             # 更新 offset
#             offset += page_size
#
#             # 若處理完畢所有資料，跳出迴圈
#             if len(query_result) < page_size:
#                 break
#
#     except Exception as e:
#         print(f"Error fetching data from database: {str(e)}")
#
#     finally:
#         session.close()  # 關閉會話


def process_category(products):
    session = get_session()
    for product in products:
        # 取得 Product 相關資訊
        product_id = product.id
        text = product.text

        # 利用 mark_category 進行品類維度標記
        matched_category = match_category(text)

        # 將維度標記更新回資料庫
        if matched_category:
            for category_name in matched_category:
                # 比對 db 中是否已有此品類維度，若無則創建維度
                category_in_db = get_category_name(session, category_name)
                if not category_in_db:
                    category_payload = category_name.copy()
                    category_create = CategoryCreate(**category_payload)
                    category_in_db = create_category(session, category_create)
                # 比對 product_id 與 category_id，並將維度標記存入資料庫
                append_category(session, product_id=product_id, category_id=category_in_db.id)


def process_sentiment(reviews):
    session = get_session()
    for review in reviews:
        # 取得 Review 相關資訊
        review_id = review.id
        text = review.text

        if text is not None:  # 如果text為空直，則不需進行情緒標記（因已預設為中立）
            sentiment = get_sentiment(1, text)  # 利用 get_sentiment 進行情緒標記

            # 將維度標記更新回資料庫
            if sentiment:
                for sentiment_name in sentiment:
                    # 比對 db 中是否已有此維度，若無則創建維度
                    sentiment_in_db = get_sentiment_name(session, sentiment_name)
                    if not sentiment_in_db:
                        sentiment_payload = sentiment_name.copy()
                        sentiment_create = SentimentCreate(**sentiment_payload)
                        sentiment_in_db = create_sentiment(session, sentiment_create)
                    # 比對review_id 與 topic_id，並將維度標記存入資料庫
                    update_review(session, review_id=review_id, review=sentiment_in_db)


def process_topic(reviews):
    session = get_session()
    for review in reviews:
        # 取得 Review 相關資訊
        review_id = review.id
        text = review.text

        if text is not None:
            matched_topics = match_topics(text)  # 利用 match_topics 進行維度標記
        else:
            text = ''  # 將 text 的值設置為空字符串
            matched_topics = match_topics(text)  # 利用 match_topics 進行維度標記

        # 將維度標記更新回資料庫
        if matched_topics:
            for topic_name in matched_topics:
                # 比對 db 中是否已有此維度，若無則創建維度
                topic_in_db = get_topic_name(session, topic_name)
                if not topic_in_db:
                    topic_payload = topic_name.copy()
                    topic_create = TopicCreate(**topic_payload)
                    topic_in_db = create_topic(session, topic_create)
                # 比對review_id 與 topic_id，並將維度標記存入資料庫
                append_topic(session, review_id=review_id, topic_id=topic_in_db.id)


@click.group()
def cli():
    pass

# cli.add_command(process_products)
cli.add_command(process_reviews)


if __name__ == '__main__':
    now = datetime.now()
    last_month = now - dateutil.relativedelta.relativedelta(months=1)  # 取的上個月的日期
    first_day_of_last_month = (date(last_month.year, last_month.month, 1)).strftime('%Y-%m-%d')
    last_day_of_last_month = (date(now.year, now.month,1) - dateutil.relativedelta.relativedelta(days=1)).strftime('%Y-%m-%d')
    first_day_dt = datetime.strptime(first_day_of_last_month, '%Y-%m-%d')
    last_day_dt = datetime.strptime(last_day_of_last_month, '%Y-%m-%d')

    cli(first_day_dt, last_day_dt)


