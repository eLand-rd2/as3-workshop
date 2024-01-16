import dataclasses

from db.sqlalchemy_models import Brand
from schemas.brand import BrandCreate


def create_brand(session, brand_data: BrandCreate):
    new_brand = Brand(**dataclasses.asdict(brand_data))

    # 提交更改
    session.add(new_brand)
    session.commit()

    print("Brand created successfully")

    return new_brand


def read_brands(session, filters=None,
                order_by=None,
                limit=None, offset=None):
    # 根據條件查詢評論
    brands = session.query(Brand).filter_by(**filters).order_by(order_by).limit(limit).offset(offset).all()

    return brands
