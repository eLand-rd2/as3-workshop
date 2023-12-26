from spiders.base import BaseSpider


class MomoSpider(BaseSpider):
    def parse_page(self, response):
        return "momo data:" + response

