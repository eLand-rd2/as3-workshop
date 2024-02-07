from sqlalchemy.orm import Session
from datetime import datetime
from db.models import Brand, Product, Review
from schemas.brand import BrandCreate
from schemas.product import ProductCreate
from crud.brand import create_or_get_brand
from crud.product import create_or_get_product

spider_data = {
            "name": "iPhone",
            "brand": {
                "name": "Apple",
                "ecommerce": 'momo'
            },
            "reviews": [
                {
                    "text": "Great product",
                    "rating": 5,
                    "post_time": "2024-01-01 00:00:00",
                    "topics": [
                        {"name": "Quality"},
                        {"name": "Price"}
                    ]
                }
            ]
        }

# 第一段测试：將爬虫数据存储到数据库中
def create_spider_data_to_db(db_session: Session, spider_data: dict):
    # 解析爬虫数据
    product_data = spider_data.get("name")
    brand_data = spider_data.get("brand")
    reviews_data = spider_data.get("reviews")

    # 检查数据库中是否已存在品牌，如果不存在则创建新品牌
    brand_name = brand_data["name"]
    ecommerce = brand_data["ecommerce"]
    brand = create_or_get_brand(db_session, brand_name, ecommerce)
    return brand

    # 检查数据库中是否已存在产品，如果不存在则创建新产品
    product = create_or_get_product(db_session, product_data)
    return product

    # 检查并创建评论以及相关主题
    for review_data in reviews_data:
        # 创建评论
        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            post_time=datetime.strptime(review_data["post_time"], "%Y-%m-%d %H:%M:%S"),
            product_id=product.id
        )
        db_session.add(review)
        db_session.commit()

# 第二段测试：测试已存储的数据能否正常获取
def test_get_reviews_with_date(db_session: Session, start_date: datetime, end_date: datetime) -> List[dict]:
    # 用來篩選出特定時間內的reviews，後續去算情緒與topic
    reviews = db_session.query(Review).filter(
        Review.post_time.between(start_date, end_date)
    ).all()

    result = []
    for review in reviews:
        result.append({
            'review_id': review.id,
            'review_text': review.text
        })

    return result

# 第三段测试：测试更新特定数据到数据库中
def test_get_data_with_date(db_session: Session, start_date: datetime, end_date: datetime) -> List[dict]:
    # 查询满足时间范围的评论信息
    reviews = db_session.query(models.Review).filter(
        and_(models.Review.post_time >= start_date, models.Review.post_time <= end_date)
    ).all()

    result = []
    for review in reviews:
        # 获取产品信息
        product_info = db_session.query(models.Product).filter_by(id=review.product_id).first()
        if product_info:
            # 获取品牌信息
            brand_info = db_session.query(models.Brand).filter_by(id=product_info.brand_id).first()
            # 获取产品对应的类别信息
            categories = [category.name for category in product_info.categories]

            # 获取评论的主题信息
            topics = [topic.name for topic in review.topics]

            result.append({
                'brand_name': brand_info.name if brand_info else None,
                'brand_ecommerce': brand_info.ecommerce if brand_info else None,
                'product_name': product_info.name,
                'product_category': categories,
                'review_text': review.text,
                'review_sentiment': review.sentiment,
                'review_rating': review.rating,
                'topics': topics
            })

    return result

    # 检查结果是否为列表
    assert isinstance(result, list)

    # 检查结果的长度是否与测试数据中的评论数量相符
    assert len(result) == 2

    # 检查每个结果项中的品牌、产品、评论等信息是否正确匹配
    assert result[0]['brand_name'] == 'Apple'
    assert result[0]['brand_ecommerce'] == 'momo'
    assert result[0]['product_name'] == 'iPhone'
    assert result[0]['product_category'] == 'Skincare'
    assert result[0]['review_text'] == 'Great product'
    assert result[0]['review_sentiment'] == '中立'  # 假设sentiment为中立
    assert result[0]['review_rating'] == 5
    assert result[0]['topics'] == ['Quality', 'Price']
