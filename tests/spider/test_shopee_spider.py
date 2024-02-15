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
    url = 'https://shopee.tw/api/v4/seller_operation/get_shop_ratings_new?limit=1&offset=0&shopid=779524889&userid=779508643'

    response = spider.request_page(url, headers=None, cookies=None)
    payload = spider.parse_page(response)
    records = spider.save_data(payload)


    # 從資料庫檢索資料
    # 檢查資料庫中是否有資料被寫入
    # assert len(records) > 0

    # 進一步檢查寫入的資料是否符合預期
    # for record in records:
    #     # 進行更多的檢查，例如檢查特定的欄位值等
    #     assert db_session.query(Product).count() == 1
    #     assert db_session.query(Review).count() == 1
    #
    #     review = get_review(db_session, review_id=1)
    #     assert review.product_id == 1
    #     assert review.product.name == 'LANCOME 蘭蔻 超未來肌因賦活露囤貨組 小黑瓶50mlx2｜官方旗艦店'
    #     assert review.post_time == '2024-02-07 07:44:52'