from spiders.momo_spider import MomoSpider
from spiders.shopee_spider import ShopeeSpider
from spiders.Ptt_spider import PttSpider

database = 'AS3_data.db'
spider_target = [
    {
        "spider_class": MomoSpider,
        "urls": [
            'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=6804476&Area=search&mdiv=403&oid=1_2&cid=index&kw=LANCOME%20%E8%98%AD%E8%94%BB'
        ]
    },
    {
        "spider_class": ShopeeSpider,
        "urls": []
    },
    {
        "spider_class": PttSpider,
        'urls': [
            'https://www.ptt.cc/bbs/MakeUp/index.html',
            'https://www.ptt.cc/bbs/BeautySalon/index.html',
            'https://www.ptt.cc/bbs/KoreaStar/index.html']
    }
]

topics = {
    "服務": ["服務", "服務品質", "服務態度", "服務態度好", "服務態度不好", "服務好", "服務不好", "服務很好",
             "服務很不好", "服務很棒", "服務很差", "服務很爛", "服務很好", "服務很不好", "服務很棒", "服務很差",
             "服務很爛", "服務很好", "服務很不好", "服務很棒", "服務很差", "服務很爛", "服務很好", "服務很不好",
             "服務很棒", "服務很差", "服務很爛"],
    "價格": ["價格", "價格便宜", "價格不便宜", "價格好", "價格不好", "價格很好", "價格很不好", "價格很棒", "價格很差",
             "價格很爛", "價格很好", "價格很不好", "價格很棒", "價格很差", "價格很爛", "價格很好", "價格很不好",
             "價格很棒", "價格很差", "價格很爛", "價格很好", "價格很不好", "價格很棒", "價格很差", "價格很爛"],
    "品質": ["品質", "品質好", "品質不好", "品質很好", "品質很不好", "品質很棒", "品質很差", "品質很爛", "品質很好",
             "品質很不好", "品質很棒", "品質很差", "品質很爛", "品質很好", "品質很不好", "品質很棒", "品質很差",
             "品質很爛", "品質很好", "品質很不好", "品質很棒", "品質很差", "品質很爛"],
}

sentiment_api_url = 'https://nlpcore.eland.com.tw/deepnlp/api/sentiment'
sentiment_api_key = 'b2kPGHkX.4xt8FSckldedMqsoX1zkduszDhOxqhC7'

file_path = ''
