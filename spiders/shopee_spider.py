from spiders.base import BaseSpider
import requests
from datetime import datetime, timedelta
import time
from crud.product import create_product, get_product
from crud.brand import create_brand, get_brand
from schemas.brand import BrandCreate
from schemas.product import ProductCreate
from crud.review import create_review, get_review, append_topic
from schemas.review import ReviewCreate



class ShopeeSpider(BaseSpider):
    def request_page(self, url, headers=None, cookies=None):
        response = requests.get(url, headers=headers, cookies=cookies).json()

        return response

    def parse_page(self, response):

        data = response.json()
        payload = []
        shopid_brand_mapping = {
            779524889: 'LANCOME蘭蔻',
            779422436: "Kiehl's契爾氏",
            37004578: '巴黎萊雅',
            6678703: '理膚寶水',
            1183: 'CeraVe適樂膚',
            37008598: 'maybelline',
            747940835: 'shu uemura植村秀',
            774925409: 'BIOTHERM-碧兒泉'
        }
        for ratings in data['data']['items']:
            stars = ratings['rating_star']
            comment = ratings['comment']
            shopid = ratings['shopid']
            ctime = ratings['ctime']
            orderid = ratings['orderid']
            brand_name = shopid_brand_mapping.get(shopid)
            utc_date_time_obj = datetime.utcfromtimestamp(ctime)

            # 時區為UTC+8
            local_timezone_offset = timedelta(hours=8)
            # 將UTC轉換為本地時間
            local_date_time_obj = utc_date_time_obj + local_timezone_offset
            # 格式化日期時間
            post_time = local_date_time_obj.strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(1)

            product_items = ratings['product_items']
            for product_item in product_items:
                product_name = product_item['name']
                time.sleep(1)

                product_dict = {

                    'ecommerce': 'shopee',
                    'brand':
                        {

                        'brand':brand_name,
                        'product': product_name,
                        },
                    'reviews': [
                        {

                            'stars': stars,
                            'comment': comment,
                            'post_time': post_time
                        }
                    ]
                }
                payload.append(product_dict)
        return payload

    def save_data(self, db_session, payload):
        for product in payload:
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

        for product in payload:
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
            for review in product['reviews']:
                review_in_db = get_review(db_session, review_id=review['id'])
                if review_in_db is None:
                    review_payload = review.copy()
                    review_payload['product_id'] = product_in_db.id
                    review_create = ReviewCreate(**review_payload)
                    create_review(db_session, review_create)
        db_session.commit()