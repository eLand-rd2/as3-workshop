from sqlalchemy.orm import Session

from db.models import Brand
from schemas.brand import BrandCreate, BrandUpdate


def read_brands(db: Session, filters=None, order_by=None, limit=None, offset=None):
    brands = db.query(Brand).filter_by(**filters).order_by(order_by).limit(limit).offset(offset).all()
    return brands


# def get_brand(db: Session, brand_id: int):
#     db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
#     return db_brand

def get_brand(db: Session, name: str):
    db_brand = db.query(Brand).filter(Brand.name == name).first()
    return db_brand


def create_or_get_brand(db: Session, brand_name: str, ecommerce: str, shop_id: str) -> Brand:
    existing_brand = db.query(Brand).filter(Brand.name == brand_name).first()
    if existing_brand:
        print("品牌名稱：" + str(brand_name) + " id: " + str(existing_brand.id))
        return existing_brand

    else:
        brand_data = BrandCreate(name=brand_name, ecommerce=ecommerce, shop_id=shop_id)
        new_brand = Brand(**brand_data.dict())
        db.add(new_brand)
        db.commit()
        db.refresh(new_brand)
        return new_brand


def create_brand(db: Session, brand: BrandCreate):
    db_brand = Brand(**brand.model_dump())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


def update_brand(db: Session, brand_id: int, brand: BrandUpdate):
    db_brand = get_brand(db, brand_id)
    if db_brand:
        update_data = brand.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_brand, key, value)
        db.commit()
        db.refresh(db_brand)
        return db_brand
    return None


def delete_brand(db: Session, brand_id: int):
    db_brand = get_brand(db, brand_id)
    if db_brand:
        db.delete(db_brand)
        db.commit()
        return db_brand
    return None
