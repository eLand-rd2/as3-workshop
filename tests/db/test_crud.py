import sys

import pytest

from crud.brand import create_brand
from db.database import get_session
from schemas.brand import BrandCreate


class TestCrud:

    def setup_method(self):
        self.session = get_session()

    def test_create_brand(self):
        payload = {
            "name": "Apple",
            "ecommerce": "apple"
        }
        model = BrandCreate(**payload)
        brand = create_brand(self.session, model)
        assert brand.id is not None
        assert brand.name == payload['name']

    def teardown_method(self):
        self.session.close()

if __name__ == '__main__':
    retcode = pytest.main(["-x", __file__])
    sys.exit(retcode)
