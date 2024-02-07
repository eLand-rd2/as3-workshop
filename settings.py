from pathlib import Path

import spiders
from spiders.momo_spider import MomoSpider
from spiders.shopee_spider import ShopeeSpider
from spiders.ptt_spider import PttSpider

BASE_DIR = Path(__file__).parent

database_url = f'sqlite:///{BASE_DIR}/as3_data.db'
spider_target = [
    {
        "spider_class": MomoSpider,
        "urls": [
            'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=6804476&Area=search&mdiv=403&oid=1_2&cid=index&kw=LANCOME%20%E8%98%AD%E8%94%BB'
        ]
    },
    {
        "spider_class": ShopeeSpider,
        "urls": [
            'https://shopee.tw/api/v4/seller_operation/get_shop_ratings_new?limit=6&offset=0&shopid=779524889&userid=779508643'
        ]
    },
    # {
    #     "spider_class": 'spiders.ptt_spider.PttSpider',
    #     'urls': [
    #         'https://www.ptt.cc/bbs/MakeUp/index.html'
    #     ]
    # }
]

categories = {
    "保養": ["精華液", "乳液", "乳霜", "精華", "凝膠"],
    "美妝": ["粉底", "粉餅", "睫毛膏", "眼線筆", "眼線液", "眼影", "眉筆", "眉粉", "修容", "打亮", "口紅"],
    "髮品": ["髮油", "洗髮精", "護髮乳", "潤髮乳", "髮膜"],
    "香水": ["香水", "淡香精"],
}

topics = {
    "運送速度": ['出貨', '到貨', '配送', '送貨', '寄件', '速度'],
    "包裝設計": ['包裝', '撒了出來', '灑出來', '破裂', '破損', '可愛', '設計感', '瓶身'],
    "價格": ['價格', '划算', '優惠', '買一送一', '便宜', '特價', '回饋', '折價券', '活動'],
    "贈品": ['贈品', '小樣', '試用品', '滿額禮'],
    "產品功效": ['吸收', '效果', '質地', '品質', '好用', '味道', '香味', '服貼', '顏色', '蓬鬆', '清爽', '豐盈', '柔順', '毛躁', '過敏']
}

sentiment_api_url = 'https://nlpcore.eland.com.tw/deepnlp/api/sentiment'
sentiment_api_key = 'b2kPGHkX.4xt8FSckldedMqsoX1zkduszDhOxqhC7'

file_path = ''
