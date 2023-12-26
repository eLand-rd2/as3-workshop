import requests


class BaseSpider:
    def request_page(self, url, headers=None, cookies=None):
        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            return response.text
        else:
            # print error message
            print(f"Error: {response.status_code}, {response.text}")
            return None

    def parse_page(self, response):
        return "base data:" + response

    def save_data(self, data):
        print(data)
        return

    def run(self, url):
        source = self.request_page(url)
        data = self.parse_page(source)
        self.save_data(data)
