from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

from db import models


def get_data_with_date(db_session: Session, start_date: datetime, end_date: datetime) -> List[dict]:
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
