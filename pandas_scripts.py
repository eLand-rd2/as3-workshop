import pandas as pd
from datetime import datetime
import dateutil.relativedelta
from report_scripts import match_topics, get_sentiment, find_matched_topic
import settings
from sqlalchemy import extract
from db.database import get_session
# from your_module import YourModel


# 從資料庫拉出資料
data = {
    'ecommerce': ['momo', 'momo', 'momo', 'momo', 'momo', 'momo', 'shopee', 'shopee', 'shopee', 'shopee', 'shopee'],
    'brand': ['Lan', 'Lan', 'LRP', 'LRP', 'LRP', 'YSL', 'GA', 'GA', 'GA', 'LOAP', 'LOAP'],
    'product': ['精華', '精華', '乳霜', '乳霜', '抗痘凝膠', '口紅', '粉底液', '粉底液', '粉底液', '乳霜', '乳液'],
    'reviews': ['服務很好', '服務很不好，價格也很貴', '服務很好，價格也很貴', '服務很不好，價格也很便宜', '服務', '價格', '價格', '品質', '服務包裝', '價格', '品質'],
    'category': ['保養', '保養', '保養', '保養', '保養', '美妝', '美妝', '美妝', '美妝', '保養', '髮品'],
    'topic': [['保養-服務', '美妝-品質'], ['保養-服務', '保養-價格', '美妝-品質'], ['保養-服務'], ['保養-價格'], ['保養-價格'], ['保養-價格'], ['美妝-品質'], ['美妝-品質'], ['美妝-品質'], ['保養-服務'], ['髮品-服務']],
    'sentiment': ['正面', '中立', '正面', '負面', '中立', '負面', '正面', '中立', '負面', '中立', '正面'],
    'rating': [3, 5, 2, 3, 4, 5, 5, 4, 3, 5, 1],
    'month': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}
df = pd.DataFrame(data)

now = datetime.now()  # 取得當前日期和時間
last_month = now+dateutil.relativedelta.relativedelta(months=-1)  # 取的上個月的日期
last_year = last_month.year
last_month = last_month.month
df = df[df['month'] == last_month]


'''
# 篩選月份
now = datetime.now()  # 取得當前日期和時間
last_month = now+dateutil.relativedelta.relativedelta(months=-1)  # 取的上個月的日期
last_year = last_month.year
last_month = last_month.month

# 建立db連線
session = get_session()
try:
    # 使用 SQLAlchemy 篩選器擷取符合條件(上個月)的資料
    query_result = (
        session.query(as3_data)
        .filter(extract('year', as3_data.post_time) == last_year)
        .filter(extract('month', as3_data.post_time) == last_month)
        .all()
    )
    # 將查詢結果轉換為 Pandas DataFrame
    df = pd.read_sql(query_result.statement, session.bind)
except Exception as e:
    print(f"Error fetching data from database: {str(e)}")
finally:
    session.close()  # 關閉會話


'''
# 維度標記
# df['topic'] = df['reviews'].apply(match_topics)  # 待刪
df['matched_topic'] = df.apply(find_matched_topic, axis=1)  # 比對 category 以及 topic
df['matched_topic'] = df['matched_topic'].apply(lambda x: '、'.join(x))  # 調整維度標記格式

# 維度標記轉為二進制
topics = settings.topics
for topic in topics:
    df[topic] = df['matched_topic'].apply(lambda x: 1 if topic in x else 0)

'''
# 進行情緒標記
docs = df['reviews']
sentiment_all = map(lambda x: get_sentiment(x[0] + 1, x[1]), enumerate(docs))
# #只擷取 sentiment_tag 的值
sentiment = [result[0]['data'][0]['sentiment_tag']for result in sentiment_all]
sentiment_series = pd.Series(sentiment, name='sentiment')
df = pd.concat([df, sentiment_series], axis=1)
'''
# 拆解 sentiment 欄位成 positve, negative, neutral三個欄位
sentiment_dummies = pd.get_dummies(df['sentiment'], prefix='sentiment', dtype=int)
df = pd.concat([df, sentiment_dummies], axis=1)



# Sheet 1 : momo與shopee兩個來源中，各品牌的總評論數&平均星等
sheet_1 = df.groupby(['ecommerce', 'brand']).agg({
    'reviews': 'count',  # 評倫則數
    'rating': 'mean',  # 當期平均星等
    'sentiment_正面': 'sum',  # 正評數
    'sentiment_負面': 'sum',  # 負評數
    'sentiment_中立': 'sum',  # 中立數
}).reset_index()
# 計算 P/N 比
sheet_1['PN_ratio'] = sheet_1.apply(lambda row:
                                    '-' if row['sentiment_負面'] == 0
                                    else 0 if row['sentiment_正面'] == 0
                                    else round(row['sentiment_正面'] / row['sentiment_負面'], 2),
                                    axis=1)
sheet_1['Group'] = "L'Oreal"  # 新增Group欄位
sheet_1 = sheet_1[['ecommerce', 'brand', 'Group', 'reviews', 'rating', 'sentiment_正面', 'sentiment_負面', 'sentiment_中立', 'PN_ratio']]  # 重新排序欄位
sheet_1 = sheet_1.sort_values(by=['ecommerce', 'brand'], key=lambda x: x.str.lower())  # 依照Brand首字母a到z排序


# sheet_2 : momo與shopee兩個來源中，各品牌的5維度分別的正評數、負評數、中立數以及PN比
all_topic_result = []
for key, value in settings.topics.items():
    print(key)
    topic_result = df[df[key] == 1]
    topic_result = topic_result.groupby(['ecommerce', 'brand']).agg({
        'sentiment_正面': 'sum',  # 正評數
        'sentiment_負面': 'sum',  # 負評數
        'sentiment_中立': 'sum',  # 中立數
    }).reset_index()
    topic_result['維度'] = key
    print(topic_result)
    all_topic_result.append(topic_result)
# 合併所有維度標記結果
sheet_2 = pd.concat(all_topic_result, ignore_index=True)
# 計算pn比
sheet_2['PN_ratio'] = sheet_2.apply(lambda row:
                                    '-' if row['sentiment_負面'] == 0
                                    else 0 if row['sentiment_正面'] == 0
                                    else round(row['sentiment_正面'] / row['sentiment_負面'], 2),
                                    axis=1)
sheet_2['Group'] = "L'Oreal"  # 新增Group欄位
sheet_2 = sheet_2[['ecommerce', 'brand', 'Group', '維度', 'sentiment_正面', 'sentiment_負面', 'sentiment_中立', 'PN_ratio']]  # 重新排序欄位
sheet_2 = sheet_2.sort_values(by=['ecommerce', 'brand'], key=lambda x: x.str.lower())  # 依照Brand首字母a到z排序


# sheet 3 : momo來源中，各品牌產品的評論內容$各評論之星等
momo_df = df[df['ecommerce'] == 'momo']    # 篩選 source = momo 的資料
sheet_3 = momo_df.groupby(['brand', 'product']).apply(lambda x: x[['reviews', 'rating', 'sentiment', 'matched_topic']].reset_index(drop=True)).reset_index()
sheet_3 = sheet_3.drop(columns=['level_2'])
sheet_3['Group'] = "L'Oreal"  # 新增Group欄位
sheet_3 = sheet_3[['brand', 'Group', 'product', 'reviews', 'rating', 'sentiment', 'matched_topic']]  # 重新排序欄位
sheet_3 = sheet_3.sort_values(by=['brand'], key=lambda x: x.str.lower())  # 依照Brand首字母a到z排序


# sheet_4 : shopee來源中，各品牌產品的評論內容$各評論之星等
shopee_df = df[df['ecommerce'] == 'shopee']    # 篩選 source = shopee 的資料
sheet_4 = shopee_df.groupby(['brand', 'product']).apply(lambda x: x[['reviews', 'rating', 'sentiment', 'matched_topic']].reset_index(drop=True)).reset_index()
sheet_4 = sheet_4.drop(columns=['level_2'])
sheet_4['Group'] = "L'Oreal"  # 新增Group欄位
sheet_4 = sheet_4[['brand', 'Group', 'product', 'reviews', 'rating', 'sentiment', 'matched_topic']]  # 重新排序欄位
sheet_4 = sheet_4.sort_values(by=['brand'], key=lambda x: x.str.lower())  # 依照Brand首字母a到z排序


# 輸出報表
# 檔案名稱
excel_filename = f'電商MonthlyReport_{last_year}_{last_month}.xlsx'

# 檔案儲存路徑
# excel_file_path = settings.file_path

# 檔案內容
with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
    # 將 sheet_1 寫入 Excel 檔案中的 '評論聲量總表' 頁籤
    sheet_1.to_excel(writer, sheet_name='評論聲量總表', index=False, header=['來源', '品牌', 'Group', '評論聲量', '當期平均星等', '正評數', '負評數', '中立數', 'P/N 比'])

    # 將 sheet_2 寫入 Excel 檔案中的 '評論類別總表' 頁籤
    sheet_2.to_excel(writer, sheet_name='評論類別總表', index=False, header=['來源', '品牌', 'Group', '討論類別', '正評數', '負評數', '中立數', 'P/N比'])

    # 將 sheet_3 寫入 Excel 檔案中的 'MOMO' 頁籤
    sheet_3.to_excel(writer, sheet_name='MOMO', index=False, header=['品牌', '產品', 'Group', '評論', '星等', '情緒標記', '維度標記'], engine='openpyxl')

    # 將 sheet_4 寫入 Excel 檔案中的 'Shopee' 頁籤
    sheet_4.to_excel(writer, sheet_name='Shopee', index=False, header=['品牌', '產品', 'Group', '評論', '星等', '情緒標記', '維度標記'], engine='openpyxl')



