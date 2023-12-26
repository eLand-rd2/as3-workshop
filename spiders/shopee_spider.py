from spiders.base import BaseSpider


class ShopeeSpider(BaseSpider):
    def parse_page(self, response):
        return "shopee data:" + response
