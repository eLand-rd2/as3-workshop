import pytest

from crud.brand import create_brand, get_brand, update_brand, delete_brand
from schemas.brand import BrandCreate, BrandUpdate


def test_create_brand(db_session):
    brand_data = BrandCreate(name="Test Brand", ecommerce="Test Ecommerce")
    brand = create_brand(db_session, brand_data)
    assert brand.id is not None
    assert brand.name == "Test Brand"


def test_get_brand(db_session):
    brand_data = BrandCreate(name="Test Brand", ecommerce="Test Ecommerce")
    brand = create_brand(db_session, brand_data)
    retrieved_brand = get_brand(db_session, brand.id)
    assert retrieved_brand is not None
    assert retrieved_brand.name == brand.name


def test_update_brand(db_session):
    brand_data = BrandCreate(name="Test Brand", ecommerce="Test Ecommerce")
    brand = create_brand(db_session, brand_data)
    updated_data = BrandUpdate(name="Updated Test Brand")
    updated_brand = update_brand(db_session, brand.id, updated_data)
    assert updated_brand is not None
    assert updated_brand.name == "Updated Test Brand"


def test_delete_brand(db_session):
    brand_data = BrandCreate(name="Test Brand", ecommerce="Test Ecommerce")
    brand = create_brand(db_session, brand_data)
    delete_brand(db_session, brand.id)
    deleted_brand = get_brand(db_session, brand.id)
    assert deleted_brand is None


if __name__ == '__main__':
    pytest.main([__file__])
