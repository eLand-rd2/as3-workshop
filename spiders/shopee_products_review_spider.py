
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
        comment = ratings['comment']
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
    {'itemid': '18672849177', 'shopid': '37004578'}, {'itemid': '23220915879', 'shopid': '37004578'}, {'itemid': '24002126203', 'shopid': '37004578'}, {'itemid': '18072092149', 'shopid': '37004578'}, {'itemid': '18472117939', 'shopid': '37004578'}, {'itemid': '16492399341', 'shopid': '37004578'}, {'itemid': '20972205434', 'shopid': '37004578'}, {'itemid': '23820915900', 'shopid': '37004578'}, {'itemid': '23630033610', 'shopid': '37004578'}, {'itemid': '14995909327', 'shopid': '37004578'}, {'itemid': '23220730338', 'shopid': '37004578'}, {'itemid': '23529990205', 'shopid': '37004578'}, {'itemid': '605517767', 'shopid': '37004578'}, {'itemid': '23216518719', 'shopid': '37004578'}, {'itemid': '10379303001', 'shopid': '37004578'}, {'itemid': '10878032362', 'shopid': '37004578'}, {'itemid': '18848374995', 'shopid': '37004578'}, {'itemid': '13037347504', 'shopid': '37004578'}, {'itemid': '13263380831', 'shopid': '37004578'}, {'itemid': '605571551', 'shopid': '37004578'}, {'itemid': '9503143019', 'shopid': '37004578'}, {'itemid': '610887637', 'shopid': '37004578'}, {'itemid': '1546905091', 'shopid': '37004578'}, {'itemid': '18968437350', 'shopid': '37004578'}, {'itemid': '12332388432', 'shopid': '37004578'}, {'itemid': '22574840087', 'shopid': '37004578'}, {'itemid': '20881789025', 'shopid': '37004578'}, {'itemid': '20582228922', 'shopid': '37004578'}, {'itemid': '23286561468', 'shopid': '37004578'}, {'itemid': '7775080780', 'shopid': '37004578'}, {'itemid': '20639772400', 'shopid': '37004578'}, {'itemid': '22776482269', 'shopid': '37004578'}, {'itemid': '18993561599', 'shopid': '37004578'}, {'itemid': '9649685396', 'shopid': '37004578'}, {'itemid': '9621703653', 'shopid': '37004578'}, {'itemid': '9913631436', 'shopid': '37004578'}, {'itemid': '605765969', 'shopid': '37004578'}, {'itemid': '20481798855', 'shopid': '37004578'}, {'itemid': '22749353523', 'shopid': '37004578'}, {'itemid': '20150549565', 'shopid': '37004578'}, {'itemid': '605827654', 'shopid': '37004578'}, {'itemid': '7816997256', 'shopid': '37004578'}, {'itemid': '23988173027', 'shopid': '37004578'}, {'itemid': '23988173027', 'shopid': '37004578'}, {'itemid': '3633730374', 'shopid': '37004578'}, {'itemid': '5333637637', 'shopid': '37004578'}, {'itemid': '8666969941', 'shopid': '37004578'}, {'itemid': '606433556', 'shopid': '37004578'}, {'itemid': '25658969449', 'shopid': '56678703'}, {'itemid': '24754467745', 'shopid': '56678703'}, {'itemid': '25453551490', 'shopid': '56678703'}, {'itemid': '21895925859', 'shopid': '56678703'}, {'itemid': '24803551546', 'shopid': '56678703'}, {'itemid': '22088368949', 'shopid': '56678703'}, {'itemid': '23261360724', 'shopid': '56678703'}, {'itemid': '4335627850', 'shopid': '56678703'}, {'itemid': '15547261900', 'shopid': '56678703'}, {'itemid': '11045072034', 'shopid': '56678703'}, {'itemid': '1601732700', 'shopid': '56678703'}, {'itemid': '964562125', 'shopid': '56678703'}, {'itemid': '1621856546', 'shopid': '56678703'}, {'itemid': '25206732823', 'shopid': '56678703'}, {'itemid': '18395643002', 'shopid': '56678703'}, {'itemid': '25952578455', 'shopid': '56678703'}, {'itemid': '20393495226', 'shopid': '56678703'}, {'itemid': '18447207593', 'shopid': '56678703'}, {'itemid': '22019220081', 'shopid': '56678703'}, {'itemid': '12381052430', 'shopid': '56678703'}, {'itemid': '15460382886', 'shopid': '56678703'}, {'itemid': '3133505475', 'shopid': '56678703'}, {'itemid': '3349514429', 'shopid': '56678703'}, {'itemid': '24658997587', 'shopid': '56678703'}, {'itemid': '23444310516', 'shopid': '56678703'}, {'itemid': '2023155553', 'shopid': '56678703'}, {'itemid': '24702577932', 'shopid': '56678703'}, {'itemid': '8062225739', 'shopid': '56678703'}, {'itemid': '17958974624', 'shopid': '56678703'}, {'itemid': '3083528292', 'shopid': '56678703'}, {'itemid': '20876127751', 'shopid': '56678703'}, {'itemid': '11132422800', 'shopid': '56678703'}, {'itemid': '964621129', 'shopid': '56678703'}, {'itemid': '965106235', 'shopid': '56678703'}, {'itemid': '2206626517', 'shopid': '56678703'}, {'itemid': '5420146977', 'shopid': '56678703'}, {'itemid': '11316368429', 'shopid': '56678703'}, {'itemid': '17545435802', 'shopid': '56678703'}, {'itemid': '19669568483', 'shopid': '56678703'}, {'itemid': '9474926253', 'shopid': '56678703'}, {'itemid': '967259615', 'shopid': '56678703'}, {'itemid': '18193493917', 'shopid': '56678703'}, {'itemid': '11425554477', 'shopid': '56678703'}, {'itemid': '10089639127', 'shopid': '56678703'}, {'itemid': '3939494669', 'shopid': '56678703'}, {'itemid': '4933482967', 'shopid': '56678703'}, {'itemid': '6039397510', 'shopid': '56678703'}, {'itemid': '24657914574', 'shopid': '56678703'}, {'itemid': '6104219885', 'shopid': '56678703'}, {'itemid': '9667227250', 'shopid': '56678703'}, {'itemid': '9667227250', 'shopid': '56678703'}, {'itemid': '4551910371', 'shopid': '56678703'}, {'itemid': '1754086527', 'shopid': '56678703'}, {'itemid': '13172145065', 'shopid': '56678703'}, {'itemid': '13256484588', 'shopid': '56678703'}, {'itemid': '14611545679', 'shopid': '56678703'}, {'itemid': '20288994964', 'shopid': '56678703'}, {'itemid': '11496656596', 'shopid': '56678703'}, {'itemid': '959499606', 'shopid': '56678703'}, {'itemid': '3379695144', 'shopid': '56678703'}, {'itemid': '959551543', 'shopid': '56678703'}, {'itemid': '21279566315', 'shopid': '56678703'}, {'itemid': '3557099148', 'shopid': '56678703'}, {'itemid': '9535381521', 'shopid': '56678703'}, {'itemid': '6712152726', 'shopid': '56678703'}, {'itemid': '9428490261', 'shopid': '56678703'}, {'itemid': '2023155553', 'shopid': '56678703'}, {'itemid': '3633887935', 'shopid': '56678703'}, {'itemid': '6549426002', 'shopid': '56678703'}, {'itemid': '7121306242', 'shopid': '56678703'}, {'itemid': '10853661020', 'shopid': '56678703'}, {'itemid': '9400054103', 'shopid': '56678703'}, {'itemid': '12417962290', 'shopid': '56678703'}, {'itemid': '959231801', 'shopid': '56678703'}, {'itemid': '20187280071', 'shopid': '56678703'}, {'itemid': '24807433409', 'shopid': '56678703'}, {'itemid': '20187280071', 'shopid': '56678703'}, {'itemid': '17486290199', 'shopid': '56678703'}, {'itemid': '8951436585', 'shopid': '56678703'}, {'itemid': '5100561760', 'shopid': '56678703'}, {'itemid': '943997711', 'shopid': '56678703'}, {'itemid': '15974312795', 'shopid': '56678703'}, {'itemid': '11788109329', 'shopid': '56678703'}, {'itemid': '20051785406', 'shopid': '56678703'}, {'itemid': '19135206240', 'shopid': '56678703'}, {'itemid': '2536237823', 'shopid': '56678703'}, {'itemid': '13687543496', 'shopid': '37008598'}, {'itemid': '11244420186', 'shopid': '37008598'}, {'itemid': '22687707210', 'shopid': '37008598'}, {'itemid': '22687707210', 'shopid': '37008598'}, {'itemid': '23455639600', 'shopid': '37008598'}, {'itemid': '6851771144', 'shopid': '37008598'}, {'itemid': '10731986869', 'shopid': '37008598'}, {'itemid': '5642567371', 'shopid': '37008598'}, {'itemid': '22237229931', 'shopid': '37008598'}, {'itemid': '1802915185', 'shopid': '37008598'}, {'itemid': '1909796732', 'shopid': '37008598'}, {'itemid': '899552567', 'shopid': '37008598'}, {'itemid': '20416758065', 'shopid': '37008598'}, {'itemid': '19338142107', 'shopid': '37008598'}, {'itemid': '19512541916', 'shopid': '37008598'}, {'itemid': '21784300788', 'shopid': '37008598'}, {'itemid': '19937812365', 'shopid': '37008598'}, {'itemid': '23550121506', 'shopid': '37008598'}, {'itemid': '25161669083', 'shopid': '37008598'}, {'itemid': '7934610538', 'shopid': '37008598'}, {'itemid': '2645485633', 'shopid': '37008598'}, {'itemid': '17175409400', 'shopid': '37008598'}, {'itemid': '4342531123', 'shopid': '37008598'}, {'itemid': '4932450621', 'shopid': '37008598'}, {'itemid': '1711713237', 'shopid': '37008598'}, {'itemid': '10344322803', 'shopid': '37008598'}, {'itemid': '8614217546', 'shopid': '37008598'}, {'itemid': '16585820866', 'shopid': '37008598'}, {'itemid': '2067721084', 'shopid': '37008598'}, {'itemid': '1924337362', 'shopid': '37008598'}, {'itemid': '651877236', 'shopid': '37008598'}, {'itemid': '1221879507', 'shopid': '37008598'}, {'itemid': '5441021021', 'shopid': '37008598'}, {'itemid': '2347063468', 'shopid': '37008598'}, {'itemid': '22665715431', 'shopid': '37008598'}, {'itemid': '22365677107', 'shopid': '37008598'}, {'itemid': '1912300105', 'shopid': '37008598'}, {'itemid': '2067777222', 'shopid': '37008598'}, {'itemid': '1559697861', 'shopid': '37008598'}, {'itemid': '4005933243', 'shopid': '37008598'}, {'itemid': '14027491378', 'shopid': '37008598'}, {'itemid': '1291124748', 'shopid': '37008598'}, {'itemid': '7233483255', 'shopid': '37008598'}, {'itemid': '12332436616', 'shopid': '37008598'}, {'itemid': '18102715607', 'shopid': '37008598'}, {'itemid': '15479810525', 'shopid': '37008598'}, {'itemid': '22887833866', 'shopid': '37008598'}, {'itemid': '22687829426', 'shopid': '37008598'}, {'itemid': '25452137639', 'shopid': '37008598'}, {'itemid': '25452137639', 'shopid': '37008598'}, {'itemid': '25302137521', 'shopid': '37008598'}, {'itemid': '23587729531', 'shopid': '37008598'}, {'itemid': '23587729531', 'shopid': '37008598'}, {'itemid': '22859456157', 'shopid': '37008598'}, {'itemid': '24057246313', 'shopid': '37008598'}, {'itemid': '3642636027', 'shopid': '37008598'}, {'itemid': '17995593747', 'shopid': '37008598'}, {'itemid': '4133619649', 'shopid': '37008598'}, {'itemid': '7657164592', 'shopid': '37008598'}, {'itemid': '22550542668', 'shopid': '37008598'}
]

result = []


for item in items:
    limit = 30
    offset = 0
    itemid = item.get('itemid')
    shopid = item.get('shopid')

    while True:
        print(f'{shopid=}, {itemid=}, {limit=}, {offset=}, {len(result)}')
        url = f'https://shopee.tw/api/v2/item/get_ratings?exclude_filter=1&filter=0&filter_size=0&flag=1&fold_filter=0&itemid={itemid}&limit={limit}&offset={offset}&relevant_reviews=false&request_source=2&shopid={shopid}&tag_filter=&type=0&variation_filters='
        response = requests.get(url=url, headers=my_headers)
        time.sleep(15)
        data = response.json()

        if data['data']['ratings'] is None:
            print('no data found')
            break
        print(len(data['data']['ratings']))

        payload = parse_data(data)
        result.extend(payload)
        save_data(payload)

        offset+=limit
