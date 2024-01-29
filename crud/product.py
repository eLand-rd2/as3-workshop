import dataclasses

from db.models import Product
from schemas.product import ProductCreate


def create_product(session, product_data: ProductCreate):
    new_product = Product(**dataclasses.asdict(product_data))

    # 提交更改
    session.add(new_product)
    session.commit()

    print("Product created successfully")

    return new_product


def read_products(session, filters=None,
                  order_by=None,
                  limit=None, offset=None):
    # 根據條件查詢評論
    products = session.query(Product).filter_by(**filters).order_by(order_by).limit(limit).offset(offset).all()

    return products
