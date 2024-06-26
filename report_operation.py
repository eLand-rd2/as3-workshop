import pandas as pd
from datetime import datetime, date
import dateutil.relativedelta
from labeling_scripts import map_brand_to_group, map_brand_to_sector
import settings
from sqlalchemy import extract
from db.database import get_session
from crud.get_data_with_date import get_data_with_date


'''
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
'''
# 篩選月份
now = datetime.now()  # 取得當前日期和時間
last_month = now - dateutil.relativedelta.relativedelta(months=1)  # 取的上個月的日期
first_day_of_last_month = (date(last_month.year, last_month.month, 1)).strftime('%Y-%m-%d')
last_day_of_last_month = (date(now.year, now.month, 1) - dateutil.relativedelta.relativedelta(days=1)).strftime('%Y-%m-%d')
first_day_dt = datetime.strptime(first_day_of_last_month, '%Y-%m-%d')
last_day_dt = datetime.strptime(last_day_of_last_month, '%Y-%m-%d')
'''

begin_date_str = input("請輸入起始日期（格式為YYYY-MM-DD）：")
try:
    # 将日期字符串转换为 datetime 对象
    begin_date_obj = datetime.strptime(begin_date_str, "%Y-%m-%d")
    print("轉換後的日期為：", begin_date_obj)
except ValueError:
    print("輸入的日期格式不正確，請重新輸入。")

end_date_str = input("請輸入起始日期（格式為YYYY-MM-DD）：")
try:
    # 将日期字符串转换为 datetime 对象
    end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d")
    print("轉換後的日期為：", end_date_obj)
except ValueError:
    print("輸入的日期格式不正確，請重新輸入。")

# 建立db連線
session = get_session()
try:
    # 使用 get_data_with_date 擷取所有符合條件(上個月)的資料
    data = get_data_with_date(session, begin_date_obj, end_date_obj)
    # 將data轉換為 Pandas DataFrame
    df = pd.DataFrame(data)
except Exception as e:
    print(f"Error fetching data from database: {str(e)}")
finally:
    session.close()  # 關閉會話

print(df.head())
# df = pd.read_excel('202401_電商評論_rawdata_0220.xlsx')

df['Group'] = df['brand'].apply(map_brand_to_group)
# df['Group'].fillna('None', inplace=True)  # 先將Group是空白的替換成'None'
df['Sector'] = df['brand'].apply(map_brand_to_sector)
# df = df[df['Group'] == "L'Oreal"]  # 篩選 Loreal Group 的資料
df['reviews'] = df['reviews'].apply(lambda x: '-' if x == '' else x)
# df['reviews'] = df['reviews'].fillna('-').astype(str)
df['topic'] = df['topic'].fillna('').astype(str)
df['topic'] = df['topic'].apply(lambda x: ', '.join(eval(x)))
df['sentiment'] = df['sentiment'].replace({'正面': 'positive', '負面': 'negative', '中立': 'neutral'})


# 維度標記轉為二進制
topics = settings.topics
for topic in topics:
    df[topic] = df['topic'].apply(lambda x: 1 if topic in x else 0)

# 拆解 sentiment 欄位成 positve, negative, neutral三個欄位
sentiment_dummies = pd.get_dummies(df['sentiment'], prefix='sentiment', dtype=int)
df = pd.concat([df, sentiment_dummies], axis=1)


# Sheet 0：各品牌的 total 表現
sheet_0 = df.groupby(['brand','Group', 'Sector']).agg({
    'reviews': 'count',  # 評倫則數
    'rating': 'mean',  # 當期平均星等
    'sentiment_positive': 'sum',  # 正評數
    'sentiment_negative': 'sum',  # 負評數
    'sentiment_neutral': 'sum',  # 中立數
}).reset_index()
sheet_0['rating'] = sheet_0['rating'].round(2)  # 當期平均星等取到小數點後兩位
sheet_0['rating'] = sheet_0['rating'].apply(lambda x: "{:.2f}".format(x))
# 計算 P/N 比
# sheet_0['PN_ratio'] = sheet_0.apply(lambda row:
#                                     '-' if row['sentiment_negative'] == 0
#                                     else 0 if row['sentiment_positive'] == 0
#                                     else "{:.1f}".format(round(row['sentiment_positive'] / row['sentiment_negative'], 1)),
#                                     axis=1)

# 計算 net sentiment
sheet_0['net_sentiment'] = ((sheet_0['sentiment_positive'] - sheet_0['sentiment_negative']) /
                       (sheet_0['sentiment_positive'] + sheet_0['sentiment_negative'] + sheet_0['sentiment_neutral'])) * 100
sheet_0['net_sentiment'] = sheet_0['net_sentiment'].round(1).astype(str) + '%'
sheet_0 = sheet_0[['brand', 'Group', 'Sector', 'reviews', 'rating', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral', 'net_sentiment']]  # 重新排序欄位
sheet_0 = sheet_0.sort_values(by=['rating'], ascending=False)  # 依照rating由大到小排序
sheet_0['Group'] = sheet_0['Group'].replace('None', '')


# Sheet 1 : momo與shopee兩個來源中，各品牌的總評論數&平均星等
sheet_1 = df.groupby(['ecommerce', 'brand', 'Group', 'Sector']).agg({
    'reviews': 'count',  # 評倫則數
    'rating': 'mean',  # 當期平均星等
    'sentiment_positive': 'sum',  # 正評數
    'sentiment_negative': 'sum',  # 負評數
    'sentiment_neutral': 'sum',  # 中立數
}).reset_index()
sheet_1['rating'] = sheet_1['rating'].round(2)  # 當期平均星等取到小數點後兩位
sheet_1['rating'] = sheet_1['rating'].apply(lambda x: "{:.2f}".format(x))
# 計算 P/N 比
# sheet_1['PN_ratio'] = sheet_1.apply(lambda row:
#                                     '-' if row['sentiment_negative'] == 0
#                                     else 0 if row['sentiment_positive'] == 0
#                                     else "{:.1f}".format(round(row['sentiment_positive'] / row['sentiment_negative'], 1)),
#                                     axis=1)

# 計算 net sentiment
sheet_1['net_sentiment'] = ((sheet_1['sentiment_positive'] - sheet_1['sentiment_negative']) /
                       (sheet_1['sentiment_positive'] + sheet_1['sentiment_negative'] + sheet_1['sentiment_neutral'])) * 100
sheet_1['net_sentiment'] = sheet_1['net_sentiment'].round(1).astype(str) + '%'
sheet_1 = sheet_1[['ecommerce', 'brand', 'Group', 'Sector', 'reviews', 'rating', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral', 'net_sentiment']]  # 重新排序欄位
sheet_1 = sheet_1.sort_values(by=['ecommerce', 'rating'], ascending=[True, False])  # 依照rating由大到小排序
sheet_1['Group'] = sheet_1['Group'].replace('None', '')


# sheet_2 : momo與shopee兩個來源中，各品牌的5維度分別的正評數、負評數、中立數以及PN比
all_topic_result = []
for key, value in settings.topics.items():
    # print(key)
    topic_result = df[df[key] == 1]
    topic_result = topic_result.groupby(['ecommerce', 'brand', 'Group', 'Sector']).agg({
        'sentiment_positive': 'sum',  # 正評數
        'sentiment_negative': 'sum',  # 負評數
        'sentiment_neutral': 'sum',  # 中立數
    }).reset_index()
    topic_result['維度'] = key
    # print(topic_result)
    all_topic_result.append(topic_result)
# 合併所有維度標記結果
sheet_2 = pd.concat(all_topic_result, ignore_index=True)
# 計算pn比
# sheet_2['PN_ratio'] = sheet_2.apply(lambda row:
#                                     '-' if row['sentiment_negative'] == 0
#                                     else 0 if row['sentiment_positive'] == 0
#                                     else "{:.1f}".format(round(row['sentiment_positive'] / row['sentiment_negative'], 1)),
#                                     axis=1)

# 計算 net sentiment
sheet_2['net_sentiment'] = ((sheet_2['sentiment_positive'] - sheet_2['sentiment_negative']) /
                       (sheet_2['sentiment_positive'] + sheet_2['sentiment_negative'] + sheet_2['sentiment_neutral'])) * 100
sheet_2['net_sentiment'] = sheet_2['net_sentiment'].round(1).astype(str) + '%'

# 定义 Sector 列的自定义类别
custom_category = ['Selective', 'Derma', 'Mass', 'Hair']
sheet_2['Sector'] = pd.Categorical(sheet_2['Sector'], categories=custom_category, ordered=True)

# 按照 'ecommerce'、'aspect' 和 'Sector' 进行排序
sheet_2 = sheet_2.sort_values(by=['ecommerce', '維度','Sector'])  # 依照Brand首字母a到z排序
sheet_2 = sheet_2[['ecommerce', '維度', 'brand', 'Group',  'Sector', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral', 'net_sentiment']]  # 重新排序欄位
sheet_2['Group'] = sheet_2['Group'].replace('None', '')


# sheet 3 : Sector為Selective中，各品牌產品的評論內容、各評論之星等
selective_df = df[df['Sector'] == 'Selective']    # 篩選 Sector = Selective 的資料
sheet_3 = selective_df.groupby(['ecommerce', 'brand', 'Group', 'product']).apply(lambda x: x[['reviews', 'rating', 'sentiment', 'topic']].reset_index(drop=True)).reset_index()
# sheet_3 = sheet_3.drop(columns=['level_2'])
sheet_3 = sheet_3[['ecommerce', 'brand', 'Group', 'product', 'reviews', 'rating', 'sentiment', 'topic']]  # 重新排序欄位
sheet_3 = sheet_3.sort_values(by=['brand', 'ecommerce'], ascending=[True, True], key=lambda x: x.str.lower())  # 依照Brand首字母a到z排序
sheet_3['Group'] = sheet_3['Group'].replace('None', '')


# sheet_4 : Sector為Derma中，各品牌產品的評論內容、各評論之星等
derma_df = df[df['Sector'] == 'Derma']    # 篩選 Sector = Derma 的資料
sheet_4 = derma_df.groupby(['ecommerce', 'brand', 'Group', 'product']).apply(lambda x: x[['reviews', 'rating', 'sentiment', 'topic']].reset_index(drop=True)).reset_index()
# sheet_4 = sheet_4.drop(columns=['level_2'])
sheet_4 = sheet_4[['ecommerce', 'brand', 'Group', 'product', 'reviews', 'rating', 'sentiment', 'topic']]  # 重新排序欄位
sheet_4 = sheet_4.sort_values(by=['brand', 'ecommerce'], ascending=[True, True], key=lambda x: x.str.lower())  # 依照Brand首字母a到z排序
sheet_4['Group'] = sheet_4['Group'].replace('None', '')


# sheet_5 : Sector為Mass中，各品牌產品的評論內容、各評論之星等
mass_df = df[df['Sector'] == 'Mass']    # 篩選 Sector = Mass 的資料
sheet_5 = mass_df.groupby(['ecommerce', 'brand', 'Group', 'product']).apply(lambda x: x[['reviews', 'rating', 'sentiment', 'topic']].reset_index(drop=True)).reset_index()
# sheet_5 = sheet_5.drop(columns=['level_2'])
sheet_5 = sheet_5[['ecommerce', 'brand', 'Group', 'product', 'reviews', 'rating', 'sentiment', 'topic']]  # 重新排序欄位
sheet_5 = sheet_5.sort_values(by=['brand', 'ecommerce'], ascending=[True, True], key=lambda x: x.str.lower())  # 依照Brand首字母a到z排序
sheet_5['Group'] = sheet_5['Group'].replace('None', '')


# sheet_6 : Sector為Hair中，各品牌產品的評論內容、各評論之星等
hair_df = df[df['Sector'] == 'Hair']    # 篩選 Sector = Hair 的資料
sheet_6 = hair_df.groupby(['ecommerce', 'brand', 'Group', 'product']).apply(lambda x: x[['reviews', 'rating', 'sentiment', 'topic']].reset_index(drop=True)).reset_index()
# sheet_6 = sheet_6.drop(columns=['level_2'])
sheet_6 = sheet_6[['ecommerce', 'brand', 'Group', 'product', 'reviews', 'rating', 'sentiment', 'topic']]  # 重新排序欄位
sheet_6 = sheet_6.sort_values(by=['brand', 'ecommerce'], ascending=[True, True], key=lambda x: x.str.lower())  # 依照Brand首字母a到z排序
sheet_6['Group'] = sheet_6['Group'].replace('None', '')


# 輸出報表
# 檔案名稱
excel_filename = f'EC_OfficialStore_MonthlyReport_2024_03_test.xlsx'
# excel_filename = f'電商MonthlyReport_{last_year}_{last_month}.xlsx'
# 檔案儲存路徑
# excel_file_path = settings.file_path

# 檔案內容
with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
    # 將 sheet_0 寫入 Excel 檔案中的 '評論聲量總表' 頁籤
    sheet_0.to_excel(writer, sheet_name='Total brand', index=False, header=['Brand', 'Group', 'Brand Sector', 'rating volume', 'avg. rating score', 'positive volume', 'negative volume', 'neutral volume', 'net sentiment'])

    # 將 sheet_1 寫入 Excel 檔案中的 '評論聲量總表' 頁籤
    sheet_1.to_excel(writer, sheet_name='By platform', index=False, header=['EC platform', 'Brand', 'Group', 'Brand Sector', 'rating volume', 'avg. rating score', 'positive volume', 'negative volume', 'neutral volume', 'net sentiment'])

    # 將 sheet_2 寫入 Excel 檔案中的 '評論類別總表' 頁籤
    sheet_2.to_excel(writer, sheet_name='By aspect', index=False, header=['EC platform', 'Aspect', 'Brand', 'Group', 'Brand Sector', 'positive volume', 'negative volume', 'neutral volume', 'net sentiment'])

    # 將 sheet_3 寫入 Excel 檔案中的 'Selective' 頁籤
    sheet_3.to_excel(writer, sheet_name='Selective', index=False, header=['EC platform', 'Brand', 'Group', 'Product', 'comment', 'rating', 'sentiment', 'aspect'], engine='openpyxl')

    # 將 sheet_4 寫入 Excel 檔案中的 'Derma' 頁籤
    sheet_4.to_excel(writer, sheet_name='Derma', index=False, header=['EC platform', 'Brand', 'Group', 'Product', 'comment', 'rating', 'sentiment', 'aspect'], engine='openpyxl')

    # 將 sheet_5 寫入 Excel 檔案中的 'Mass' 頁籤
    sheet_5.to_excel(writer, sheet_name='Mass', index=False, header=['EC platform', 'Brand', 'Group', 'Product', 'comment', 'rating', 'sentiment', 'aspect'], engine='openpyxl')

    # 將 sheet_6 寫入 Excel 檔案中的 'Hair' 頁籤
    sheet_6.to_excel(writer, sheet_name='Hair', index=False, header=['EC platform', 'Brand', 'Group', 'Product', 'comment', 'rating', 'sentiment', 'aspect'], engine='openpyxl')


