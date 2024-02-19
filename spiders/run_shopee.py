from spiders.shopee_spider import ShopeeSpider

result =[]

spider = ShopeeSpider()
shops = ['56678703']
# , '779422436', '37004578', '56678703', '70001183', '37008598', '747940835', '774925409'

for shop in shops:
    for n in range(0, 901, 100) :
        print(f'{shop=}, {n=}, {len(result)}')
        url = f'https://shopee.tw/api/v4/seller_operation/get_shop_ratings_new?limit=100&offset={n}&shopid={shop}&userid=779508643'
        response = spider.request_page(url, headers=None, cookies=None)
        payload = spider.parse_page(response)
        result.extend(payload)
        spider.save_data(payload)
