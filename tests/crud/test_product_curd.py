import pytest

from crud.product import create_product, get_product, update_product, delete_product
from schemas.product import ProductCreate, ProductUpdate


def test_create_product(db_session):
    product_data = ProductCreate(name="Test Product", rating=4.5, brand_id=1)  # 根据需要调整
    product = create_product(db_session, product_data)
    assert product.id is not None
    assert product.name == "Test Product"


def test_get_product(db_session):
    product_data = ProductCreate(name="Test Product", rating=4.5, brand_id=1)
    product = create_product(db_session, product_data)
    retrieved_product = get_product(db_session, product.id)
    assert retrieved_product is not None
    assert retrieved_product.name == product.name


def test_update_product(db_session):
    product_data = ProductCreate(name="Test Product", rating=4.5, brand_id=1)
    product = create_product(db_session, product_data)
    updated_data = ProductUpdate(name="Updated Test Product", rating=5.0)
    updated_product = update_product(db_session, product.id, updated_data)
    assert updated_product is not None
    assert updated_product.name == "Updated Test Product"


def test_delete_product(db_session):
    product_data = ProductCreate(name="Test Product", rating=4.5, brand_id=1)
    product = create_product(db_session, product_data)
    delete_product(db_session, product.id)
    deleted_product = get_product(db_session, product.id)
    assert deleted_product is None


if __name__ == '__main__':
    pytest.main([__file__])
