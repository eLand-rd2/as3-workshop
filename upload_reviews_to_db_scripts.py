from crud.upload_reviews_to_db import create_or_get_brand, create_or_get_product, create_review
import pandas as pd
from db.database import get_session
from schemas.review import ReviewCreate

def upload_reviews_to_database(session, review_data_list: list):
    for review_data in review_data_list:
        # 检查并创建品牌
        brand = create_or_get_brand(session, review_data['brand'], review_data['ecommerce'])

        # 检查并创建产品
        product = create_or_get_product(session, brand.id, review_data['title'])

        # 创建评论
        review_create = ReviewCreate(text=review_data['content'],
                                     post_time=review_data['post_time'],
                                     rating=review_data['used_count'],
                                     product_id=product.id)
        create_review(session, review_create)

# 示例用法
if __name__ == "__main__":
    # 假设您有一个 review_data_list 包含了要上传的评论数据
    df = pd.read_excel("momo_rawdata_for_upload.xlsx")
    df['content'] = df['content'].fillna('').astype(str)
    print(df.head())

    # 连接到数据库
    session = get_session()

    # 将 DataFrame 转换为列表以便上传到数据库
    review_data_list = df.to_dict('records')
    print(review_data_list)

    # 上传评论数据到数据库
    upload_reviews_to_database(session, review_data_list)

    # 关闭数据库连接
    session.close()
