from sqlalchemy.orm import Session

from db.models import Brand
from schemas.brand import BrandCreate, BrandUpdate
from db.database import get_session


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

def update_brand_name(db: Session, brand_id: int, new_name: str):
    # 1. 使用品牌 ID 查询数据库，找到要更新的品牌
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()

    # 2. 如果找到了品牌，将其名称更新为指定的内容
    if db_brand:
        db_brand.ecommerce = new_name

        # 3. 提交更改到数据库中
        db.commit()
        return {"msg": "Brand name updated successfully"}

    return {"msg": "Brand not found"}

def delete_brand(db: Session, brand_id: int):
    db_brand = get_brand(db, brand_id)
    if db_brand:
        db.delete(db_brand)
        db.commit()
        return db_brand
    return None


if __name__ == '__main__':
    session = get_session()
    brands_to_update = {
        1: "Shopee",
        2: "Shopee",
        3: "Shopee",
        4: "Shopee",
        5: "Shopee",
        6: "Shopee",
        7: "Shopee",
        8: "Shopee"
    }
    for id, brand_name in brands_to_update.items():
        update_brand_name(session, id, brand_name)
        print(f'update {id=}')
    session.close()
