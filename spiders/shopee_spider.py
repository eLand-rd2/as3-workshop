from spiders.base import BaseSpider
import requests

class ShopeeSpider(BaseSpider):
    def request_page(self, url, headers=None, cookies=None):
        response = requests.get(url, headers=headers, cookies=cookies).json()

        return response

    def parse_page(self, response):
        for rating in response['data']['ratings']:
            comment = rating['comment']

            return 'shopee data\n' + comment
