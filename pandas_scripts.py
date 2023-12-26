import pandas as pd
from datetime import datetime

# 從資料庫拉出資料
data = {
    'source': ['momo', 'momo', 'momo', 'momo', 'momo', 'momo', 'shopee', 'shopee', 'shopee', 'shopee', 'shopee'],
    'brand': ['Lan', 'Lan', 'LRP', 'LRP', 'LRP', 'Cerave', 'Lan', 'Lan', 'Lan', 'LOAP', 'LOAP'],
    'product': ['小黑瓶', '小黑瓶', '萬能霜', '萬能霜', '抗痘凝膠', 'PM乳', '小黑瓶', '零粉感', '零粉感', '紫熨斗', '紫熨斗'],
    'comment': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
    'rating': ['3', '5', '2', '3', '4', '5', '5', '4', '3', '5', '1'],
    'sentiment': ['正面', '正面', '負面', '負面', '正面', '正面', '中立', '中立', '中立', '正面', '負面'],
    'dimension_A': ['1', '0', '0', '1', '1', '0', '1', '1', '0', '0', '0'],
    'dimension_B': ['0', '1', '0', '1', '1', '0', '0', '1', '1', '0', '1'],
    'dimension_C': ['0', '0', '1', '1', '1', '0', '0', '0', '0', '1', '1'],
    'dimension_D': ['1', '1', '0', '0', '1', '0', '0', '0', '1', '0', '0'],
    'dimension_E': ['1', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0'],
    'month': ['12', '12', '12', '12', '12', '12', '12', '12', '12', '12', '12']
}
df = pd.DataFrame(data)



# 資料清理
# 篩選月份
now = datetime.now()  # 取得當前日期和時間
month_now = now.month  # 提取當前月份
df['month'] = pd.to_numeric(df['month'])  # 將 month 欄位轉換為數字
df = df[df['month'] == month_now]

# 將'rating'列轉為浮點數
df['rating'] = df['rating'].astype(float)

# 新增dimension_included欄位，填入每一則評論內容被標記的維度 (for sheet_3 和 sheet_4)
df['dimension_included'] = df.apply(lambda row: ';'.join(dim for dim, val in zip(['Dimension_A', 'Dimension_B', 'Dimension_C', 'Dimension_D', 'Dimension_E'], row[8:]) if val == '1'), axis=1)

# 拆解 sentiment 欄位成 positve, negative, neutral三個欄位
sentiment_dummies = pd.get_dummies(df['sentiment'], prefix='sentiment')
df = pd.concat([df, sentiment_dummies], axis=1)


# Sheet 1 : momo與shopee兩個來源中，各品牌的總評論數&平均星等
sheet_1 = df.groupby(['source', 'brand']).agg({
    'comment': 'count',  # 評倫則數
    'rating': 'mean',  # 當期平均星等
    'sentiment_正面': 'count',  # 正評數
    'sentiment_負面': 'count',  # 負評數
    'sentiment_中立': 'count',  # 中立數
}).reset_index()
# 計算 P/N 比
sheet_1['PN ratio'] = (sheet_1['sentiment_正面']/sheet_1['sentiment_負面']).apply(lambda x: round(x, 2) if x > 0 else 0 if x == 0 else '-')

# 重新排序欄位
sheet_1 = sheet_1[['source', 'brand', 'comment', 'rating', 'sentiment_正面', 'sentiment_負面', 'sentiment_中立', 'PN ratio']]
sheet_1 = sheet_1.sort_values(by=['source', 'brand'], key=lambda x: x.str.lower())  # 依照Brand首字母a到z排序


# sheet_2 : momo與shopee兩個來源中，各品牌的5維度分別的正評數、負評數、中立數以及PN比


# sheet 3 : momo來源中，各品牌產品的評論內容$各評論之星等
momo_df = df[df['source'] == 'momo']    # 篩選 source = momo 的資料
sheet_3 = momo_df.groupby(['brand', 'product']).apply(lambda x: x[['comment', 'rating', 'sentiment', 'dimension_included']].reset_index(drop=True)).reset_index()
sheet_3 = sheet_3.drop(columns=['level_2'])


# sheet_4 : shopee來源中，各品牌產品的評論內容$各評論之星等
shopee_df = df[df['source'] == 'shopee']    # 篩選 source = shopee 的資料
sheet_4 = shopee_df.groupby(['brand', 'product']).apply(lambda x: x[['comment', 'rating', 'sentiment', 'dimension_included']].reset_index(drop=True)).reset_index()
sheet_4 = sheet_4.drop(columns=['level_2'])


# 輸出報表
excel_filename = f'電商MonthlyReport_2024_{month_now}.xlsx'
with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
    # 將 sheet_1 寫入 Excel 檔案中的 '評論聲量總表' 頁籤
    sheet_1.to_excel(writer, sheet_name='評論聲量總表', index=False, header=['來源', '品牌', '評論聲量', '當期平均星等', '正評數', '負評數', '中立數', 'P/N 比'])

    # 將 sheet_2 寫入 Excel 檔案中的 '評論類別總表' 頁籤
    # sheet_2.to_excel(writer, sheet_name='評論類別總表', index=False, header=['來源', '品牌', '討論類別', '正評數', '負評數', '中立數', 'P/N比'])

    # 將 sheet_3 寫入 Excel 檔案中的 'MOMO' 頁籤
    sheet_3.to_excel(writer, sheet_name='MOMO', index=False, header=['品牌', '產品', '評論', '星等', '情緒標記', '維度標記'])

    # 將 sheet_4 寫入 Excel 檔案中的 'Shopee' 頁籤
    sheet_4.to_excel(writer, sheet_name='Shopee', index=False, header=['品牌', '產品', '評論', '星等', '情緒標記', '維度標記'])
