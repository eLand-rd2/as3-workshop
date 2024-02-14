import pytest
from sqlalchemy.orm import Session
from datetime import datetime
from db.models import Brand, Product, Review
from schemas.brand import BrandCreate
from schemas.product import ProductCreate
from crud.brand import create_or_get_brand
from crud.product import create_or_get_product

# 第一段测试：测试爬虫数据是否能正常存储到数据库中
def test_store_crawler_data_to_db(db_session: Session):
    # 模拟爬虫数据
    brand_name = "Apple"
    ecommerce = "momo"
    product_name = "iPhone"
    category = "Skincare"

    # 创建品牌
    brand = create_or_get_brand(db_session, brand_name, ecommerce)
    assert isinstance(brand, Brand)

    # 创建产品
    product = create_or_get_product(db_session, product_name, category, brand.id)
    assert isinstance(product, Product)

    # 创建评论
    review_text = "Great product"
    rating = 5
    post_time = datetime.now()
    review = Review(text=review_text, rating=rating, post_time=post_time, brand_id=brand.id, product_id=product.id)
    db_session.add(review)
    db_session.commit()

    # 检查数据是否成功存储到数据库中
    assert db_session.query(Brand).filter_by(name=brand_name).first() is not None
    assert db_session.query(Product).filter_by(name=product_name).first() is not None
    assert db_session.query(Review).filter_by(text=review_text).first() is not None

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
                'brand': brand_info.name if brand_info else None,
                'ecommerce': brand_info.ecommerce if brand_info else None,
                'product': product_info.name,
                'category': categories,
                'reviews': review.text,
                'sentiment': review.sentiment,
                'rating': review.rating,
                'topic': topics
            })

    return result

    # 检查结果是否为列表
    assert isinstance(result, list)

    # 检查结果的长度是否与测试数据中的评论数量相符
    assert len(result) == 2

    # 检查每个结果项中的品牌、产品、评论等信息是否正确匹配
    assert result[0]['brand'] == 'Apple'
    assert result[0]['ecommerce'] == 'momo'
    assert result[0]['product'] == 'iPhone'
    assert result[0]['category'] == 'Skincare'
    assert result[0]['reviews'] == 'Great product'
    assert result[0]['sentiment'] == '中立'  # 假设sentiment为中立
    assert result[0]['rating'] == 5
    assert result[0]['topic'] == ['Quality', 'Price']
