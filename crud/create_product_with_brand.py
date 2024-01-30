from crud.product import create_product, get_product
from crud.brand import create_brand, get_brand
from schemas.brand import BrandCreate
from schemas.product import ProductCreate
# from 廣興的程式碼 import 爬文資料 (payload)


def test_create_product_with_brand(db_session, payload):
    for product in payload:
        print('存入' + product)
        product_in_db = get_product(db_session, product_id=product['id'])
        if product_in_db is None:
            brand_id = product['brand']['id']
            brand_in_db = get_brand(db_session, brand_id=brand_id)
            if brand_in_db is None:
                brand_payload = product['brand'].copy()
                brand = BrandCreate(**brand_payload)
                brand_in_db = create_brand(db_session, brand)
            product_payload = product.copy()
            product_payload['brand_id'] = brand_in_db.id
            product_create = ProductCreate(**product_payload)
            create_product(db_session, product_create)
    db_session.commit()

    print('產品資料儲存完畢')
