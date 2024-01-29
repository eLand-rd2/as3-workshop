import pytest
from crud.product import create_product, get_product
from crud.brand import create_brand, get_brand
from crud.review import create_review, get_review, append_topic
from crud.topic import get_topic, create_topic
from db.models import Topic
from schemas.brand import BrandCreate
from schemas.product import ProductCreate
from db import Brand, Product, Review
from schemas.review import ReviewCreate
from schemas.topic import TopicCreate


@pytest.fixture
def payload():
    return [
        {
            "id": 1,
            "name": "iPhone",
            "brand": {
                "id": 1,
                "name": "Apple",
                "ecommerce": 'momo'
            },
            "reviews": [
                {
                    "id": 1,
                    "text": "Great product",
                    "rating": 5,
                    "post_time": "2024-01-01 00:00:00",
                    "topics": [
                        {"id": 1, "name": "Quality"},
                        {"id": 2, "name": "Price"}
                    ]
                }
            ]
        },
        {
            "id": 2,
            "name": "Galaxy",
            "brand": {
                "id": 2,
                "name": "Samsung",
                "ecommerce": 'momo'
            },
            "reviews": [
                {
                    "id": 2,
                    "text": "Bad product",
                    "rating": 1,
                    "post_time": "2024-01-01 00:00:00",
                    "topics": [
                        {"id": 1, "name": "Quality"},
                        {"id": 3, "name": "Service"}
                    ]
                }
            ]
        }
    ]


def test_create_product_with_brand(db_session, payload):
    for product in payload:
        product_in_db = get_product(db_session, product_id=product['id'])
        if not product_in_db:
            brand_id = product['brand']['id']
            brand_in_db = get_brand(db_session, brand_id=brand_id)
            if not brand_in_db:
                brand_payload = product['brand'].copy()
                brand = BrandCreate(**brand_payload)
                brand_in_db = create_brand(db_session, brand)
            product_payload = product.copy()
            product_payload['brand_id'] = brand_in_db.id
            product_create = ProductCreate(**product_payload)
            create_product(db_session, product_create)
    db_session.commit()

    assert db_session.query(Product).count() == 2
    assert db_session.query(Brand).count() == 2

    product = get_product(db_session, product_id=1)
    assert product.brand_id == 1
    assert product.brand.name == 'Apple'
    assert product.brand.ecommerce == 'momo'

    product = get_product(db_session, product_id=2)
    assert product.brand_id == 2
    assert product.brand.name == 'Samsung'
    assert product.brand.ecommerce == 'momo'


def test_create_review_with_product(db_session, payload):
    for product in payload:
        product_in_db = get_product(db_session, product_id=product['id'])
        if not product_in_db:
            brand_id = product['brand']['id']
            brand_in_db = get_brand(db_session, brand_id=brand_id)
            if not brand_in_db:
                brand_payload = product['brand'].copy()
                brand = BrandCreate(**brand_payload)
                brand_in_db = create_brand(db_session, brand)
            product_payload = product.copy()
            product_payload['brand_id'] = brand_in_db.id
            product_create = ProductCreate(**product_payload)
            create_product(db_session, product_create)
        for review in product['reviews']:
            review_in_db = get_review(db_session, review_id=review['id'])
            if not review_in_db:
                review_payload = review.copy()
                review_payload['product_id'] = product_in_db.id
                review_create = ReviewCreate(**review_payload)
                create_review(db_session, review_create)
    db_session.commit()

    assert db_session.query(Product).count() == 2
    assert db_session.query(Review).count() == 2

    review = get_review(db_session, review_id=1)
    assert review.product_id == 1
    assert review.product.name == 'iPhone'

    review = get_review(db_session, review_id=2)
    assert review.product_id == 2
    assert review.product.name == 'Galaxy'


def test_create_review_with_product_and_topic(db_session, payload):
    for product in payload:
        product_in_db = get_product(db_session, product_id=product['id'])
        if not product_in_db:
            brand_id = product['brand']['id']
            brand_in_db = get_brand(db_session, brand_id=brand_id)
            if not brand_in_db:
                brand_payload = product['brand'].copy()
                brand = BrandCreate(**brand_payload)
                brand_in_db = create_brand(db_session, brand)
            product_payload = product.copy()
            product_payload['brand_id'] = brand_in_db.id
            product_create = ProductCreate(**product_payload)
            create_product(db_session, product_create)
        for review in product['reviews']:
            review_in_db = get_review(db_session, review_id=review['id'])
            if not review_in_db:
                review_payload = review.copy()
                review_payload['product_id'] = product_in_db.id
                review_create = ReviewCreate(**review_payload)
                create_review(db_session, review_create)
            for topic in review['topics']:
                topic_in_db = get_topic(db_session, topic_id=topic['id'])
                if not topic_in_db:
                    topic_payload = topic.copy()
                    topic_create = TopicCreate(**topic_payload)
                    topic_in_db = create_topic(db_session, topic_create)
                append_topic(db_session, review_id=review_in_db.id, topic_id=topic_in_db.id)
    db_session.commit()
    assert db_session.query(Product).count() == 2
    assert db_session.query(Review).count() == 2
    assert db_session.query(Topic).count() == 3

    review = get_review(db_session, review_id=1)
    assert review.product_id == 1
    assert review.product.name == 'iPhone'
    assert len(review.topics) == 2
    assert review.topics[0].name == 'Quality'
    assert review.topics[1].name == 'Price'

    review = get_review(db_session, review_id=2)
    assert review.product_id == 2
    assert review.product.name == 'Galaxy'
    assert len(review.topics) == 2
    assert review.topics[0].name == 'Quality'
    assert review.topics[1].name == 'Service'

