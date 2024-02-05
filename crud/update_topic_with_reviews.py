
from crud.product import create_product, get_product
from crud.review import create_review, get_review, append_topic
from crud.topic import get_topic
from schemas.product import ProductCreate
from schemas.review import ReviewCreate
from schemas.topic import TopicCreate

def create_review_with_product_and_topic(db_session, payload):
    for product in payload:
        print('確認' + product + '是否已存在')
        product_in_db = get_product(db_session, product_id=product['id'])
        if product_in_db is None:
            print('已確認先前不存在' + product + '，正在對照該產品的brand')
            brand_id = product['brand']['id']
            brand_in_db = get_brand(db_session, brand_id=brand_id)
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
        for review in product['reviews']:
            print('正在存入' + review)
            review_in_db = get_review(db_session, review_id=review['id'])
            if review_in_db is None:
                review_payload = review.copy()
                review_payload['product_id'] = product_in_db.id
                review_create = ReviewCreate(**review_payload)
                create_review(db_session, review_create)
                print('已成功存入' + review)
            for topic in review['topics']:
                print('正在存入' + topic)
                topic_in_db = get_topic(db_session, topic_id=topic['id'])
                if topic_in_db is None:
                    topic_payload = topic.copy()
                    topic_create = TopicCreate(**topic_payload)
                    topic_in_db = create_topic(db_session, topic_create)
                    print('已成功存入' + topic)
                append_topic(db_session, review_id=review_in_db.id, topic_id=topic_in_db.id)
    db_session.commit()

    print('評論命中之主題資料更新完畢')