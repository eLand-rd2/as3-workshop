
from db.database import get_session
import requests
from datetime import datetime, timedelta
import time
from crud.product import create_or_get_product
from crud.brand import create_or_get_brand
from crud.review import create_or_get_review


def parse_data(data):

    payload = []
    shopid_brand_mapping = {
        '779524889': 'LANCOME',
        '779422436': "Kiehl's",
        '37004578': 'Loreal paris',
        '56678703': 'La Roche-Posay',
        '70001183': 'CeraVe',
        '37008598': 'maybelline',
        '747940835': 'shu uemura',
        '774925409': 'BIOTHERM'
    }
    for ratings in data['data']['ratings']:
        stars = ratings['rating_star']
        comment = str(ratings['comment'])
        shopid = str(ratings['shopid'])
        ctime = ratings['ctime']
        itemid = str(ratings['itemid'])
        orderid = str(ratings['orderid'])
        brand_name = shopid_brand_mapping.get(shopid)
        utc_date_time_obj = datetime.utcfromtimestamp(ctime)

        # 時區為UTC+8
        local_timezone_offset = timedelta(hours=8)
        # 將UTC轉換為本地時間
        local_date_time_obj = utc_date_time_obj + local_timezone_offset
        # 格式化日期時間
        post_time = local_date_time_obj.strftime("%Y-%m-%d")
        time.sleep(1)

        product_items = ratings['product_items']
        for product_item in product_items:
            product_name = product_item['name']
            time.sleep(1)

            product_dict = {
                'ecommerce': 'shopee',
                'brand':
                    {
                        'name': brand_name,
                        'product': product_name,
                        'shop_id': shopid,
                    },
                'product':
                    {
                        'name': product_name,
                        'item_id': itemid,

                    },
                'review':
                    {
                        'rating': stars,
                        'text': comment,
                        'post_time': post_time,
                        'sentiment': '中立',
                        'order_id': orderid
                    }

            }
            payload.append(product_dict)

    return payload

def save_data(payload):
    db_session = get_session()
    for product_info in payload:
        brand_name = product_info['brand']['name']
        ecommerce = product_info['ecommerce']
        shop_id = product_info['brand']['shop_id']
        brand_in_db = create_or_get_brand(db_session, brand_name, ecommerce, shop_id)
        product_name = product_info['product']['name']
        item_id = product_info['product']['item_id']
        product_in_db = create_or_get_product(db_session, product_name, brand_in_db.id, item_id)


        review_text = product_info['review']['text']
        review_post_time = product_info['review']['post_time']
        review_rating = product_info['review']['rating']
        review_sentiment = product_info['review']['sentiment']
        review_order_id = product_info['review']['order_id']
        create_or_get_review(db_session, product_in_db.id, review_text, review_post_time, review_rating, review_sentiment, review_order_id)

    db_session.close()

my_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Cookie': 'SPC_F=LSx1SEt5lfeSPtPip0yiYnhX15053bLR; REC_T_ID=a790e354-b375-11ee-bead-7a05fa6d30ef; SPC_R_T_ID=mdFJAyEuI/cwmVOUbu4yJ9riE1Z8hLdudMTWZ2gSf2RYFmxvhjyrJaScOtcV793Kifpa3JW/utlpklerML0enPWYBNOG55Spd+0vV34dzbslYRVvcj5zzvAtPH8ZFLNzG81ThkQvbjWtREoMpz7JtCoLH8acyh0BhwfsLG3iQCg=; SPC_R_T_IV=TWxwUUtoQXpYRDA0RW1LbA==; SPC_T_ID=mdFJAyEuI/cwmVOUbu4yJ9riE1Z8hLdudMTWZ2gSf2RYFmxvhjyrJaScOtcV793Kifpa3JW/utlpklerML0enPWYBNOG55Spd+0vV34dzbslYRVvcj5zzvAtPH8ZFLNzG81ThkQvbjWtREoMpz7JtCoLH8acyh0BhwfsLG3iQCg=; SPC_T_IV=TWxwUUtoQXpYRDA0RW1LbA==; _gcl_au=1.1.364911333.1705302841; _fbp=fb.1.1705302841941.119810701; _ga_E1H7XE0312=GS1.1.1705993085.4.1.1705994531.0.0.0; _ga=GA1.2.245782118.1705302842; __LOCALE__null=TW; _med=refer; csrftoken=rVuYBF8iqUcITnJoE5ze8lKBQ1blyaSp; _sapid=7c1de95d45c64d38546d78efa290432c9bf6a88afb96cba94b915f60; SPC_SI=gn6nZQAAAABxejRmSEhPZX8ptQAAAAAAYnM0VWE0MUQ=; SPC_SEC_SI=v1-RXB1R1hjbjZvc0x5blo1RP2iI78b9rH0wC8w9DRl4Y2R36VdzkZELQ6SIpnFb8DwSXDqLJ7YvYnjf9EB/Ss8GBAPuf2cATHkT4xwTjJZwkk=; _QPWSDCXHZQA=4ddd6b2d-c2c6-4d98-b45c-d4d8120700d2; REC7iLP4Q=3e8aa926-4dcf-4a80-b94a-7ec475bf6376; _gid=GA1.2.1344465249.1705977423; shopee_webUnique_ccd=HCuIUZaHUCeFeDxCQBDRTw%3D%3D%7CWnn%2BBsTy64bRrF0gjXxj131cjtKHH4jJ4VJYJnqPtm7G%2FDMVNNgDI3gz%2B6p7lnS3NXiuWr%2FbZos%3D%7Cxq9VRKrLoEukDdaD%7C08%7C3; ds=abdd3961b8b07a556cc7f637e824573b; AMP_TOKEN=%24NOT_FOUND; SPC_CLIENTID=TFN4MVNFdDVsZmVTufmryflgnqykhjeb; SPC_P_V=VSUFu4caQLGlF2lKrfSskaWVnUBLe/74cquBFtSLssO8wD5DDliE3PJQP7XUEsUeYanJteMBYbhopkY4VVXVgjDxBbh5Pti6Bz5PwPSIqFLMIehglbGjg6BTFQEfZ7Vm3U8GRz977OGqILLxuG+0GiBHPs0KHlkGHWbbfOgFmAE=; SPC_EC=.NnlqS04wcUFwdWgzQ2NNYi7MVYYcSFE4cEKvRZa5F2j9O4vys4gpLiQZg5O2qEyxrYDOMj6Hi/UZq57/2Q574oaB2EiLNJ21D0QEh7y4x57ZK7fO4v0vPBzgSLD8NOobEeRUIkSEDUu97bfQ3o0w9bwfJMtNLmEZjlWneUq43n9qlCI8s5xZLkcICCYj8WWPEh8fGY8iI06YoEawX+FWEw==; SPC_ST=.NnlqS04wcUFwdWgzQ2NNYi7MVYYcSFE4cEKvRZa5F2j9O4vys4gpLiQZg5O2qEyxrYDOMj6Hi/UZq57/2Q574oaB2EiLNJ21D0QEh7y4x57ZK7fO4v0vPBzgSLD8NOobEeRUIkSEDUu97bfQ3o0w9bwfJMtNLmEZjlWneUq43n9qlCI8s5xZLkcICCYj8WWPEh8fGY8iI06YoEawX+FWEw==; SPC_U=42893816'
}

items = [
{'itemid': '1391561895', 'shopid': '70001183'}, {'itemid': '1183332796', 'shopid': '70001183'}, {'itemid': '21947708806', 'shopid': '70001183'},  {'itemid': '1183316743', 'shopid': '70001183'}, {'itemid': '22356848691', 'shopid': '70001183'},
{'itemid': '24657657910', 'shopid': '70001183'}, {'itemid': '25761751548', 'shopid': '70001183'}, {'itemid': '24912023188', 'shopid': '70001183'}, {'itemid': '23467901907', 'shopid': '70001183'}, {'itemid': '23172543713', 'shopid': '70001183'},
{'itemid': '23609520252', 'shopid': '70001183'}, {'itemid': '23085165826', 'shopid': '70001183'}, {'itemid': '21585858047', 'shopid': '70001183'}, {'itemid': '17750272496', 'shopid': '70001183'}, {'itemid': '12589718542', 'shopid': '70001183'}
]

result = []


for item in items:
    limit = 50
    offset = 0
    itemid = item.get('itemid')
    shopid = item.get('shopid')

    while True:
        print(f'{shopid=}, {itemid=}, {limit=}, {offset=}, {len(result)}')
        url = f'https://shopee.tw/api/v2/item/get_ratings?exclude_filter=1&filter=0&filter_size=0&flag=1&fold_filter=0&itemid={itemid}&limit={limit}&offset={offset}&relevant_reviews=false&request_source=2&shopid={shopid}&tag_filter=&type=0&variation_filters='
        response = requests.get(url=url, headers=my_headers)
        time.sleep(10)
        data = response.json()

        if data['data']['ratings'] is None:
            print('no data found')
            break
        print(len(data['data']['ratings']))

        payload = parse_data(data)
        result.extend(payload)
        save_data(payload)

        offset+=limit

        if offset == 500:
            break
