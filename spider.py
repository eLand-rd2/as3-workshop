import requests


def get_ptt_data(ptt_url, ptt_headers: dict = None):
    if not ptt_headers:
        ptt_headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
    response = requests.get(ptt_url, headers=ptt_headers)
    if response.status_code == 200:
        return response
    else:
        # print error message
        print(f"Error: {response.status_code}, {response.text}")
        return None


if __name__ == '__main__':
    # prepare spider params
    ptt_url = 'https://www.ptt.cc/bbs/MakeUp/index3850.html'
    ptt_headers = {}

    # make a request to get html response
    ptt_response = get_ptt_data(ptt_url, ptt_headers)
    #print(ptt_response.text)

    # parse html in response
from bs4 import BeautifulSoup
soup = BeautifulSoup(ptt_response.text,features="html.parser")

for entry in soup.select('.r-ent'):
    print(entry.select('.title')[0].text,entry.select('.date')[0].text)
    # save data to db
