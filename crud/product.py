from sqlalchemy.orm import Session

from db.models import Product, Category
from schemas.product import ProductCreate, ProductUpdate, ProductBase


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_or_get_product(db: Session, product: ProductBase, brand_id):
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        # print("品牌名稱：" + str(product_data.name) + "id:" +  int(existing_product.id))
        return existing_product
    else:
        new_product = Product(name=product.name,
                                     brand_id=brand_id,
                              item_id=product.item_id)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, order_by='product_id', limit=100, offset=0):
    query_result = db.query(Product).filter(Product.category.is_(None)).order_by(order_by).limit(limit).offset(offset).all()
    return query_result

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    return None


def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return {"msg": "Product deleted"}

def append_category(db: Session, product_id, category_id): # Serena更新category用
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db_category = db.query(Category).filter(Category.id == category_id).first()

    if db_product and db_category:
        db_product.topics.append(db_category)
        db.commit()
        db.refresh(db_product)
        return db_product
    return None
