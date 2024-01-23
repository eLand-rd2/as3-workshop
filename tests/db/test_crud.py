import datetime

from sqlalchemy.orm import Session

from crud.reviews import create_review
from db.database import get_session
from schemas.brand import BrandRead
from schemas.product import ProductRead
from schemas.review import ReviewsCreate

# pytest fixture

class TestCrud:
    def __init__(self, _session: Session):
        self.session = _session

        self.brand = BrandRead(id=1, name='test')
        self.product = ProductRead(id=1, name='test', brand=self.brand)

    def test_create(self):
        review_data = ReviewsCreate(
            product=self.product,
            text='test',
            rating=5.0,
            post_time=datetime.datetime.strptime("2023-12-25 12:00:00", "%Y-%m-%d %H:%M:%S"),
            sentiment='中立',
            topics=None
        )
        result = create_review(self.session, review_data)
        assert result.text == 'test'
        assert result.rating == 5.0
        assert result.product == self.product

    def test_read(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass


if __name__ == '__main__':
    with get_session() as session:
        crud_test = TestCrud(session)
        crud_test.test_create()
