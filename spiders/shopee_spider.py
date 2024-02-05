from spiders.base import BaseSpider
import requests
import time

class ShopeeSpider(BaseSpider):
    def request_page(self, url, headers=None, cookies=None):
        response = requests.get(url, headers=headers, cookies=cookies).json()

        return response

    def parse_page(self, response):

        data = response.json()
        product_list = []

        for ratings in data['data']['items']:
            stars = ratings['rating_star']
            comment = ratings['comment']
            shopid = ratings['shopid']
            ctime = ratings['ctime']
            utc_date_time_obj = datetime.utcfromtimestamp(ctime)

            # 時區為UTC+8
            local_timezone_offset = timedelta(hours=8)
            # 將UTC轉換為本地時間
            local_date_time_obj = utc_date_time_obj + local_timezone_offset
            # 格式化日期時間
            creat_time = local_date_time_obj.strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(1)

            product_items = ratings['product_items']
            for product_item in product_items:
                product_name = product_item['name']
                time.sleep(1)

                product_dict = {
                    'shopid': shopid,
                    'product': product_name,
                    'stars': stars,
                    'comment': comment,
                    'creat_time': creat_time
                }
                product_list.append(product_dict)
        return product_list

    def save_data(self, data):
