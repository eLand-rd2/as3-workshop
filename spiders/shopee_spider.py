from spiders.base import BaseSpider
import requests

class ShopeeSpider(BaseSpider):
    def request_page(self, url, headers=None, cookies=None):
        response = requests.get(url, headers=headers, cookies=cookies).json()

        return response

    def parse_page(self, response):

        stars = []
        comments = []

        for ratings_content in response['data']['ratings']:
            star = ratings_content['rating_star']
            stars.append(star)
            comment = ratings_content['comment']
            comments.append(comment)

            return 'shopee data:'+ ''.join(stars) + ''.join(comments)
