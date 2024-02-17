import pytest

from db.database import get_session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from db import Base, Review, Product
from spiders.shopee_spider import ShopeeSpider
# from crud.review import create_review, get_review, append_topic

# @pytest.fixture
# def db_session():
#     # 創建測試用的資料庫連接
#     engine = create_engine(database_url)
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     Base.metadata.create_all(bind=engine)
#
#     # 創建測試用的 session
#     db = TestingSessionLocal()
#
#     # 返回 session
#     yield db
#
#     # 在測試結束後清除資料庫
#     Base.metadata.drop_all(bind=engine)

def test_run_ShopeeSpider():
    spider = ShopeeSpider()
    shops = ['779524889', '779422436', '37004578', '56678703']
    # , '70001183', '37008598', '747940835', '774925409'

    for shop in shops:
        for n in range(0, 901, 100) :
            url = f'https://shopee.tw/api/v4/seller_operation/get_shop_ratings_new?limit=100&offset={n}&shopid={shop}&userid=779508643'
            response = spider.request_page(url, headers=None, cookies=None)
            payload = spider.parse_page(response)
            spider.save_data(payload)


