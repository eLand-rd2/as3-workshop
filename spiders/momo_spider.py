from spiders.base import BaseSpider
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from crud.product import create_product, get_product
from crud.brand import create_brand, get_brand
from schemas.brand import BrandCreate
from schemas.product import ProductCreate
from crud.review import create_review, get_review, append_topic
from schemas.review import ReviewCreate

class MomoSpider(BaseSpider):
    def request_page(self, url):
        driver = webdriver.Firefox()

        opts = Options()
        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        opts.add_argument("user-agent={}".format(ua))

        driver.get(url)

        button = driver.find_element(By.CLASS_NAME, 'goodsCommendLi')
        button.click()

        time.sleep(5)

        response = driver.page_source
        driver.close()
        return response

    def parse_page(self, response):
        payload = []
        product_dict = {}

        product_name = response.find_element(By.ID, 'osmGoodsName').text
        brand_content = response.find_element(By.CLASS_NAME, 'brandTrackBtn')
        brand_name = brand_content.find_element(By.TAG_NAME, 'a').text

        comment_contents = response.find_elements(By.CLASS_NAME, 'reviewCard')
        for comment_content in comment_contents:
            comment = comment_content.find_element(By.CLASS_NAME, 'CommentContainer').text
            infoinner = comment_content.find_element(By.CLASS_NAME, 'InfoInner')
            post_time = infoinner.find_element(By.CLASS_NAME, 'Info').text
            rating = infoinner.find_element(By.CLASS_NAME, 'RatingStarGroup')
            stars = rating.get_attribute('score')
            time.sleep(2)

            product_dict = {
                'ecommerce': 'momo',
                'brand':
                    {
                        'brand': brand_name,
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
