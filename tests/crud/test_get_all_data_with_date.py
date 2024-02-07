from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

from db import models

from test_mixed_curd import (
    test_create_product_with_brand,
    test_create_review_with_product,
    test_create_review_with_product_and_topic
)

@pytest.fixture
def create_test_data():
    # 运行创建测试数据的测试
    test_create_product_with_brand()
    test_create_review_with_product()
    test_create_review_with_product_and_topic()

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
