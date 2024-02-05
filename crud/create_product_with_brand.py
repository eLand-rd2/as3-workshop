from crud.product import create_product, get_product
from crud.brand import create_brand, get_brand
from schemas.brand import BrandCreate
from schemas.product import ProductCreate
# from 廣興的程式碼 import 爬文資料 (payload)


def create_product_with_brand(db_session, payload):
    for product in payload:
        print('確認' + product + '是否已存在')
        product_in_db = get_product(db_session, product_id=product['id'])
        print('確認資料庫內存在' + product + '，其id為:' + str(product['id']))
        if product_in_db is None:
            print('已確認資料庫內不存在' + product + '，正在對照該產品的brand')
            brand_id = product['brand']['id']
            brand_in_db = get_brand(db_session, brand_id=brand_id)
            print('確認資料庫內存在' + str(product['brand']) + '，其id為:' + str(brand_id))
            if brand_in_db is None:
                print('已確認該產品的' + str(product['brand']) + '不存在資料庫，正在存入中...')
                brand_payload = product['brand'].copy()
                brand = BrandCreate(**brand_payload)
                brand_in_db = create_brand(db_session, brand)
                print('已將' + str(product['brand']) + '新增進資料庫')
            product_payload = product.copy()
            product_payload['brand_id'] = brand_in_db.id
            product_create = ProductCreate(**product_payload)
            create_product(db_session, product_create)
            print('已將' + product + '新增進資料庫')

    db_session.commit()

    print('產品資料儲存完畢')
