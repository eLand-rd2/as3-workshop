from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import union_all
from sqlalchemy_settings import EcommerceReviews
from sqlalchemy_settings import ReviewsCategory


# Create
def create_review(session, brand, source, product, common, rating, month, sent, topic):
    try:
        ecommerce_review = EcommerceReviews(brand=brand, source=source, product=product, common=common, rating=rating,
                                            month=month)
        reviews_category = ReviewsCategory(brand=brand, source=source, product=product, common=common, sent=sent,
                                           month=month)
        reviews_category.set_topic(topic)  # set_topic 是用於資料庫存儲前的轉換 如果topic是list就轉成JSON

    # Add objects to the session
        session.add(ecommerce_review)
        session.add(reviews_category)

    # Commit the transaction
        session.commit()
        print("Review created successfully")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Failed to create review: {e}")


# Read
def get_reviews_by_brand(session, brand):
    try:
        ecommerce_reviews_query = session.query(EcommerceReviews).filter_by(brand=brand).all()
        reviews_category_query = session.query(ReviewsCategory).filter_by(brand=brand).all()

        # 使用 union_all 將兩個查詢合併
        combined_query = union_all(ecommerce_reviews_query, reviews_category_query)

        # 執行合併後的查詢
        result = session.execute(combined_query).fetchall()
        return result

    except SQLAlchemyError as e:
        print(f"Failed to retrieve reviews: {e}")
        return []


def get_reviews_by_month(session, month):
    try:
        ecommerce_reviews_query = session.query(EcommerceReviews).filter_by(month=month).all()
        reviews_category_query = session.query(ReviewsCategory).filter_by(month=month).all()

        # 使用 union_all 將兩個查詢合併
        combined_query = union_all(ecommerce_reviews_query, reviews_category_query)

        # 執行合併後的查詢
        result = session.execute(combined_query).fetchall()
        return result

    except SQLAlchemyError as e:
        print(f"Failed to retrieve reviews: {e}")
        return []


# Update
def update_review_rating(session, review_id, new_rating):
    pass


# Delete
def delete_review(session, review_id):
    pass
