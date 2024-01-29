from spiders.base import BaseSpider
from bs4 import BeautifulSoup


class PttSpider(BaseSpider):
    def parse_page(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        titles = []  # 創建一個空列表，用於存儲所有的 titles
        top_bar = soup.find_all('div', {'id': 'topbar'})
        labels = top_bar[0].find_all('a')[1]  # 取出看板名

        for entry in soup.select('.r-ent'):
            title_text = entry.select('.title')[0].text
            titles.append(title_text)  # 將每個 title 加入列表
        return labels.text + ''.join(titles)  # 使用逗號將所有 titles 連接為一個字串並返回
