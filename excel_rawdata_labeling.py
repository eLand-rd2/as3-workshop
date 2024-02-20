from report_scripts import match_topics, get_sentiment
import pandas as pd

df = pd.read_excel('MOMO.xlsx')


# 維度標記
df['reviews'] = df['reviews'].fillna('').astype(str)
df['topic'] = df['reviews'].apply(match_topics)
df['topic'] = df['topic'].apply(lambda x: '、'.join(x))  # 調整維度標記格式


# 情緒標記
for index, row in df.iterrows():
    review = row['reviews']
    if review != '':
        sentiment_result = get_sentiment(1, review)
        df.at[index, 'sentiment'] = sentiment_result
    else:
        df.at[index, 'sentiment'] = '中立'


# 輸出成excel
excel_filename = f'MOMO_labeling.xlsx'
with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='rawdata', index=False)

