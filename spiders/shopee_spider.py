from db.database import get_session
from spiders.base import BaseSpider
import requests
from datetime import datetime, timedelta
import time
from crud.product import create_or_get_product
from crud.brand import create_or_get_brand
from crud.review import create_review, create_or_get_review
from schemas.review import ReviewCreate



class ShopeeSpider(BaseSpider):
    def request_page(self, url, headers=None, cookies=None):
        response = requests.get(url, headers=headers, cookies=cookies)
        time.sleep(15)

        return response

    def parse_page(self, response):

        data = response.json()
        payload = []
        shopid_brand_mapping = {
            '779524889': 'LANCOME',
            '779422436': "Kiehl's",
            '37004578': 'Loreal paris',
            '56678703': 'La Roche-Posay',
            '70001183': 'CeraVe',
            '37008598': 'maybelline',
            '747940835': 'shu uemura',
            '774925409': 'BIOTHERM'
        }
        for ratings in data['data']['items']:
            stars = ratings['rating_star']
            comment = str(ratings['comment'])
            shopid = str(ratings['shopid'])
            ctime = ratings['ctime']
            itemid = str(ratings['itemid'])
            orderid = str(ratings['orderid'])
            brand_name = shopid_brand_mapping.get(shopid)
            utc_date_time_obj = datetime.utcfromtimestamp(ctime)

            # 時區為UTC+8
            local_timezone_offset = timedelta(hours=8)
            # 將UTC轉換為本地時間
            local_date_time_obj = utc_date_time_obj + local_timezone_offset
            # 格式化日期時間
            post_time = local_date_time_obj.strftime("%Y-%m-%d")
            time.sleep(1)

            product_items = ratings['product_items']
            for product_item in product_items:
                product_name = product_item['name']
                time.sleep(1)

                product_dict = {
                    'ecommerce': 'shopee',
                    'brand':
                        {
                            'name': brand_name,
                            'product': product_name,
                            'shop_id': shopid,
                        },
                    'product':
                        {
                            'name': product_name,
                            'item_id': itemid,

                        },
                    'review':
                        {
                            'rating': stars,
                            'text': comment,
                            'post_time': post_time,
                            'sentiment': '中立',
                            'order_id': orderid
                        }

                }
                payload.append(product_dict)
        return payload

    def save_data(self, payload):
        db_session = get_session()
        for product_info in payload:
            brand_name = product_info['brand']['name']
            ecommerce = product_info['ecommerce']
            shop_id = product_info['brand']['shop_id']
            brand_in_db = create_or_get_brand(db_session, brand_name, ecommerce, shop_id)
            product_name = product_info['product']['name']
            item_id = product_info['product']['item_id']
            product_in_db = create_or_get_product(db_session, product_name, brand_in_db.id, item_id)


            review_text = product_info['review']['text']
            review_post_time = product_info['review']['post_time']
            review_rating = product_info['review']['rating']
            review_sentiment = product_info['review']['sentiment']
            review_order_id = product_info['review']['order_id']
            create_or_get_review(db_session, product_in_db.id, review_text, review_post_time, review_rating, review_sentiment, review_order_id)

        db_session.close()
