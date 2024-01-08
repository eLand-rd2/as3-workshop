from spiders.base import BaseSpider
from bs4 import BeautifulSoup

class PttSpider(BaseSpider):
    def parse_page(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        titles = []  # 創建一個空列表，用於存儲所有的 titles

        for entry in soup.select('.r-ent'):
            title_text = entry.select('.title')[0].text
            titles.append(title_text)  # 將每個 title 加入列表
        return "ptt data:" + ''.join(titles)  # 使用逗號將所有 titles 連接為一個字串並返回



