import dataclasses

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import union_all
from db.sqlalchemy_models import Brand
from db.sqlalchemy_models import Product
from db.sqlalchemy_models import Ecommerce
from db.sqlalchemy_models import BrandRating
from db.sqlalchemy_models import Rating
from db.sqlalchemy_models import Reviews
from db.sqlalchemy_models import Topic
from db.sqlalchemy_models import Sentiment
from db.sqlalchemy_models import Month



@dataclasses.dataclass
class EcommerceReviews:
    id: int
    brand: str
    ecommerce: str
    product: str
    common: str
    rating: float
    month: int


# Create
def create_review(session, review_data):
    # 檢查 review_data 中的值是否符合要求
    rating = review_data.get('rating')
    month = review_data.get('month')
    brand = review_data.get('brand')
    ecommerce = review_data.get('ecommerce')
    product = review_data.get('product')
    reviews_text = review_data.get('reviews')
    sentiment = review_data.get('sentiment', "中立") #預設值 如果一開始再加入前沒有情緒跟TOPICS的話會套用預設值
    topics = review_data.get('topics', "Nan")

    # assert rating in range(1, 6), and is float
    if not (isinstance(rating, float) and rating in range(1, 6)):
        raise ValueError("Rating must be a float between 1 and 5")
    # assert month in range(1, 13), and is integer
    if not (isinstance(month, int) and month in range(1, 13)):
        raise ValueError("Month must be an integer between 1 and 12")
    # assert brand is string
    if not (isinstance(brand, str)):
        raise ValueError("Brand must be a string")
    # assert source is string
    if not (isinstance(ecommerce, str)):
        raise ValueError("Ecommerce must be a string")
    # assert product is string
    if not (isinstance(product, str)):
        raise ValueError("Product must be a string")
    # assert reviews_text is string
    if not (isinstance(reviews_text, str)):
        raise ValueError("Reviews must be a string")
    # assert sentiment is string
    if not (isinstance(sentiment, str)):
        raise ValueError("Sentiment must be a string")
    # assert topics is string
    if not (isinstance(topics, str)):
        raise ValueError("Topics must be a string")

    # 創建 Reviews 實例
    new_review = Reviews(
        text=reviews_text,
        topics=topics,
        sentiment=Sentiment(name=sentiment),
        product=Product(
            name=product,
            brand=Brand(name=brand),
            rating=Rating(value=rating)
        )
    )

    # 提交更改
    session.add(new_review)
    session.commit()

    print("Reviews created successfully")



# Read
def read_reviews_by_brand(session, brand_name):
    # 根據品牌名稱查詢相關的評論
    reviews = session.query(Reviews).\
        join(Product).join(Brand).\
        filter(Brand.name == brand_name).all()

    return reviews

def read_reviews_by_month(session, target_month):
    # 根據特定月份查詢相關的評論
    reviews = session.query(Reviews).\
        filter(extract('month', Reviews.timestamp) == target_month).all()

    return reviews


# Update
def update_topics_and_sentiments(session, review_data):
    for review_info in review_data:
        review_text = review_info['text']
        topics = review_info['topics']
        sentiment_value = review_info['sentiment']

        # 根據 review_text 查找相應的 Reviews
        review = session.query(Reviews).filter_by(text=review_text).first()

        if review:
            # 更新 Topic
            review.topics = topics

            # 更新 Sentiment
            sentiment = session.query(Sentiment).filter_by(name=sentiment_value).first()

            if not sentiment:
                sentiment = Sentiment(name=sentiment_value)

            review.sentiment = sentiment

            # 提交更改
            session.commit()
        else:
            print(f"Review with text '{review_text}' not found.")

# Delete
def delete_review(session, review_id):
    pass