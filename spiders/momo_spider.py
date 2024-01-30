from spiders.base import BaseSpider
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import settings
import time

class MomoSpider(BaseSpider):
    def request_page(self, url):
        driver = webdriver.Firefox()

        opts = Options()
        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        opts.add_argument("user-agent={}".format(ua))

        driver.get(url)

        button = driver.find_element(By.CLASS_NAME, 'goodsCommendLi')
        button.click()

        time.sleep(5)

        response = driver.page_source
        driver.close()
        return response

    def parse_page(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        comments = []
        brand_names = []
        star_ratings = []
        comment_contents = soup.find_all('div', {'class': 'reviewCard'})
        brand_elements = soup.find_all('div',{'id':'bt_2_layout_NAV'})


        for brand_element in brand_elements:
            brand_name = brand_element.find('h1').text
            brand_names.append(brand_name)

        for comment_content in comment_contents:
            comment = comment_content.select('.CommentContainer')[0].text
            comments.append(comment)



        return 'momodata:\n' + '\n'.join(brand_names) + '\n'.join(comments)

