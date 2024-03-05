from sqlalchemy.orm import Session
from db.models import Brand, Product, Review
from schemas.review import ReviewCreate


def create_or_get_brand(db: Session, brand_name: str, brand_ecommerce: str):
    brand = db.query(Brand).filter(Brand.name == brand_name).filter(Brand.ecommerce == brand_ecommerce).first()
    if not brand:
        brand = Brand(name=brand_name, ecommerce=brand_ecommerce)
        db.add(brand)
        db.commit()
    return brand

def create_or_get_product(db: Session, brand_id: int, product_name: str):
    product = db.query(Product).filter(Product.name == product_name).first()
    if not product:
        product = Product(name=product_name, brand_id=brand_id)
        db.add(product)
        db.commit()
    return product

def create_review(db: Session, review_data: ReviewCreate):
    review = Review(**review_data.dict())
    db.add(review)
    db.commit()
    return review


