import dataclasses
from typing import List

from schemas.review import ReviewsCreate, ReviewsUpdate
from db.sqlalchemy_models import Reviews


# Create
def create_review(session, review_data: ReviewsCreate):
    new_review = Reviews(**dataclasses.asdict(review_data))

    # 提交更改
    session.add(new_review)
    session.commit()

    print("Reviews created successfully")

    return new_review


def read_reviews(session, filters=None,
                 order_by=None,
                 limit=None, offset=None):
    # 根據條件查詢評論
    reviews = session.query(Reviews).filter_by(**filters).order_by(order_by).limit(limit).offset(offset).all()

    return reviews


# Read
def read_reviews_by_brand(session, brand_id,
                          order_by='post_time', limit=10, offset=0):
    # 根據品牌名稱查詢相關的評論
    return read_reviews(session, filters={'brand_id': brand_id},
                        order_by=order_by, limit=limit,
                        offset=offset)


def read_reviews_by_post_time(session, begin_time, end_time,
                              order_by='post_time', limit=10, offset=0):
    # 根據時間查詢相關的評論
    return read_reviews(session, filters={'post_time': (begin_time, end_time)},
                        order_by=order_by, limit=limit,
                        offset=offset)


# Update
def update_topics_and_sentiments(session, review_data_rows: List[ReviewsUpdate]):
    for review_data in review_data_rows:
        review_text = review_data.text
        topics = review_data.topics
        sentiment_value = review_data.sentiment

        # 根據 id 查找相應的 Reviews
        review_in_db = session.query(Reviews).get(review_data.id)

        if review_in_db:
            review_in_db.topics = topics
            review_in_db.sentiment = sentiment_value
            review_in_db.text = review_text
            # 提交更改
            session.commit()
        else:
            print(f"Review with text '{review_text}' not found.")


# Delete
def delete_review(session, review_id):
    pass
