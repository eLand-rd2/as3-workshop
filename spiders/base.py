import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import settings

class BaseSpider:
    def __init__(self):
        self.ua = UserAgent()  #每次查詢初始化 UserAgent

    def request_page(self, url, headers=None, cookies=None):
            response = requests.get(surl, headers=headers, cookies=cookies)
            headers = {'user-agent': self.ua.random
                       }
            if response.status_code == 200:
                return response.text
            else:
                # print error message
                print(f"Error: {response.status_code}, {response.text}")
                return None

    def parse_page(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        return "base data:" + soup.text

    def save_data(self, data):
        print(data)
        return

    def run(self, url):
        source = self.request_page(url)
        data = self.parse_page(source)
        self.save_data(data)

if __name__ == '__main__':
    spider = BaseSpider()
    spider.run(settings.base_url)