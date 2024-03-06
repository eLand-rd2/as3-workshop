from pathlib import Path

import spiders
# from spiders.momo_spider import MomoSpider
# from spiders.shopee_spider import ShopeeSpider
# from spiders.ptt_spider import PttSpider

BASE_DIR = Path(__file__).parent

database_url = 'mysql+pymysql://yijialee:livlytakemymoney@172.18.30.31:3306/analysis_temp'
spider_target = [
    # {
    #     "spider_class": MomoSpider,
    #     "urls": [
    #         'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=6804476&Area=search&mdiv=403&oid=1_2&cid=index&kw=LANCOME%20%E8%98%AD%E8%94%BB'
    #     ]
    # },
     {
        "spider_class": 'spider.shopee_spider.ShopeeSpider',
        "urls":[
            'https://shopee.tw/api/v4/seller_operation/get_shop_ratings_new?limit={limit}&offset={offset}&shopid={shopid}&userid=779508643'
        ],
         'url_pattern':  "",
         'items': [{'itemid' : '24803551546','shopid':'56678703'}, {'itemid':'20187280071','shopid':'56678703'}]
    }
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
    "包裝設計": ['新包裝', '聯名', '可愛', '設計', '瓶身', '合作'],
    "價格": ['價格', '划算', '優惠', '買一送一', '便宜', '特價', '回饋', '折價券', '活動'],
    "贈品": ['贈品', '小樣', '試用品', '滿額禮'],
    "產品功效": ['吸收', '效果', '質地', '品質', '好用', '有用', '有效', '味道', '香味', '無香', '清爽', '厚重' '不油', '舒服', '乾淨', '保濕度', '很保濕', '舒緩', '泛紅',
                 '滋潤', '不會乾', '不會很乾', '乾澀', '乾癢', '乾燥', '黏膩', "粘膩", '刺激', '細緻', '滑嫩', '顆粒', '平滑', '光滑', '緊繃', '延展', '推勻',
                 '痘痘', '粉刺', '毛孔', '黑頭', '紋路', '細紋', '過敏', '脫皮', '乾裂', '龜裂', '改善', '痘疤', '淡疤', '淡斑',
                 '浮粉', '貼妝', '服貼', '服帖', '斑駁', '脫妝', '持久', '顯白', '顯黃', '顯黑', '暗沉', '暗沈', '持色', '掉妝', '顏色',
                 '蓬鬆', '豐盈', '柔順', '毛躁', '脫髮', '生髮', ]
}

sentiment_api_url = 'https://nlpcore.eland.com.tw/deepnlp/api/sentiment'
sentiment_api_key = 'b2kPGHkX.4xt8FSckldedMqsoX1zkduszDhOxqhC7'

file_path = ''
