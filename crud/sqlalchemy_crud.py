import dataclasses

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import union_all
from db.sqlalchemy_models import EcommerceReviews
from db.sqlalchemy_models import ReviewsCategory


@dataclasses.dataclass
class EcommerceReviews:
    id: int
    brand: str
    source: str
    product: str
    common: str
    rating: float
    month: int


# Create
def create_review(session, brand, source, product, common, rating, month, sent, topic):
    # assert rating in range(1, 6), and is float
    if not (isinstance(rating, float) and rating in range(1, 6)):
        raise ValueError("Rating must be a float between 1 and 5")

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
        return EcommerceReviews(id=ecommerce_review.id, brand=ecommerce_review.brand,
                                source=ecommerce_review.source, product=ecommerce_review.product,
                                common=ecommerce_review.common, rating=ecommerce_review.rating,
                                month=ecommerce_review.month)
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
        return ReviewsCategory(id=result.id, brand=result.brand, source=result.source, product=result.product,
                               common=result.common, sent=result.sent, month=result.month, topic=result.topic)


    except SQLAlchemyError as e:
        print(f"Failed to retrieve reviews: {e}")
        return []


def get_reviews_by_month(session, month) -> list[EcommerceReviews]:
    try:
        ecommerce_reviews_query = session.query(EcommerceReviews).filter_by(month=month).all()
        reviews_category_query = session.query(ReviewsCategory).filter_by(month=month).all()

        # 使用 union_all 將兩個查詢合併
        combined_query = union_all(ecommerce_reviews_query, reviews_category_query)

        # 執行合併後的查詢
        result = session.execute(combined_query).fetchall()
        return ReviewsCategory(id=result.id, brand=result.brand, source=result.source, product=result.product,
                               common=result.common, sent=result.sent, month=result.month, topic=result.topic)

    except SQLAlchemyError as e:
        print(f"Failed to retrieve reviews: {e}")
        return []


# Update
def update_review_rating(session, review_id, new_rating):
    pass


# Delete
def delete_review(session, review_id):
    pass
