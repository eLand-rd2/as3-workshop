import datetime

from sqlalchemy.orm import Session

from crud.reviews import (
    create_review,
    read_reviews_by_brand,
    read_reviews_by_post_time,
    update_topics_and_sentiments
)
from db.database import get_session
from schemas.brand import BrandRead
from schemas.product import ProductRead
from schemas.review import ReviewsCreate, ReviewsUpdate
# 從schemas import class進來 如果不import進來會怎樣

# pytest fixture

class TestCrud:
   # def __init__(self, _session: Session):
   #      self.session = _session
   #
   #      self.brand = BrandRead(id=1, name='test')
   #      self.product = ProductRead(id=1, name='test', brand=self.brand)


    def setup_method(self):
        self.session = get_session()

        self.brand = BrandRead(id=1, name='test')
        self.product = ProductRead(id=1, name='test', brand=self.brand)

    def test_create(self):
        review_data = ReviewsCreate(
            product=self.product,
            text='test',
            rating=5.0,
            post_time=datetime.datetime.strptime("2023-12-25 12:00:00",
                                                 "%Y-%m-%d %H:%M:%S"),
            sentiment='中立',
            topics=None
        )

        # 調用被測試的 read_reviews_by_brand 函式
        result = create_review(self.session, review_data)
        assert result.text == 'test'
        assert result.rating == 5.0
        assert result.product == self.product

    def test_read_reviews_by_brand(self):
        # 創建屬於指定品牌的評論
        review_data_1 = ReviewsCreate(
            product=self.product,
            text='test1',
            rating=5.0,
            post_time=datetime.datetime.strptime("2023-12-24 12:00:00",
                                                 "%Y-%m-%d %H:%M:%S"),
            sentiment='中立',
            topics=None
        )
        create_review(self.session, review_data_1)

        # 創建屬於其他品牌的評論
        other_brand = BrandRead(id=2, name='other_brand')
        other_product = ProductRead(id=2, name='other_product', brand=other_brand)
        review_data_2 = ReviewsCreate(
            product=other_product,
            text='test2',
            rating=4.0,
            post_time=datetime.datetime.strptime("2023-12-26 12:00:00",
                                                 "%Y-%m-%d %H:%M:%S"),
            sentiment='正面',
            topics=None
        )
        create_review(self.session, review_data_2)

        # 調用被測試的 read_reviews_by_brand 函式
        result = read_reviews_by_brand(self.session, brand_id=self.brand.id, limit=10)

        # 進行斷言，確保擷取的評論數量和內容符合預期
        assert len(result) == 1  # 只有一條屬於指定品牌的評論
        assert result[0].text == 'test1'
        assert result[0].product.brand == self.brand  # 確保品牌符合預期

    def read_reviews_by_post_time(self):
        # 創建屬於指定時間段的評論
        review_data_1 = ReviewsCreate(
            product=self.product,
            text='test1',
            rating=5.0,
            post_time=datetime.datetime.strptime("2023-12-24 12:00:00",
                                                 "%Y-%m-%d %H:%M:%S"),
            sentiment='中立',
            topics=None
        )
        create_review(self.session, review_data_1)

        # 創建屬於其他時間段的評論
        review_data_2 = ReviewsCreate(
            product=self.product,
            text='test2',
            rating=4.0,
            post_time=datetime.datetime.strptime("2023-11-26 12:00:00",
                                                 "%Y-%m-%d %H:%M:%S"),
            sentiment='正面',
            topics=None
        )
        create_review(self.session, review_data_2)

        # 調用被測試的 read_reviews_by_post_time 函式
        begin_time = datetime.datetime.strptime("2023-12-01 00:00:00",
                                                "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime("2023-12-31 23:59:59",
                                              "%Y-%m-%d %H:%M:%S")
        result = read_reviews_by_post_time(self.session, begin_time, end_time, limit=10)

        # 進行斷言，確保擷取的評論數量和內容符合預期
        assert len(result) == 1  # 只有一條屬於指定時間段的評論
        assert result[0].text == 'test1'
        assert result[0].product.brand == self.brand  # 確保品牌符合預期

    def test_update_topics_and_sentiments(self):
        #創建一條既有的評論
        review_data_1 = ReviewsCreate(
            product=self.product,
            text='test1',
            rating=5.0,
            post_time=datetime.datetime.strptime("2023-12-24 12:00:00",
                                                 "%Y-%m-%d %H:%M:%S"),
            sentiment='中立',
            topics=None
        )
        existing_review = create_review(self.session, review_data_1)
        # 創建用來更新的資訊
        review_data_renew = ReviewsUpdate(
            id=existing_review.id,
            text='test1',
            sentiment='負面',
            topics='價格'
        )
        # 調用被測試的 read_reviews_by_post_time 函式
        result = update_topics_and_sentiments(self.session, review_data_renew)

        # 進行斷言，確保擷取的評論數量和內容符合預期
        assert result.text == 'test1'
        assert result.sentiment == '負面'
        assert result.topics == '價格'

    def test_delete(self):
        pass

    def teardown_method(self):
        self.session.close()

# # If you run this file directly, execute the tests
# if __name__ == '__main__':
#     pytest.main([__file__])

if __name__ == '__main__':
    with get_session() as session:
        crud_test = TestCrud(session)
        crud_test.test_create()
        crud_test.test_read_reviews_by_brand()
        crud_test.read_reviews_by_post_time()
        crud_test.test_update_topics_and_sentiments()
