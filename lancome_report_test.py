from report_scripts import match_topics, get_sentiment
import pandas as pd

df = pd.read_excel('lancome_data.xlsx')
# 維度標記
df['review'] = df['review'].fillna('')
df['topic'] = df['review'].apply(match_topics)


# 情緒標記
# rows = df.shape[0]
# for id in range(1, rows):
#     reviews = df['review'].tolist()
#     sentiment = get_sentiment(id, df['review'][id])
#     df['sentiment'] = df['sentiment'].apply(sentiment)

# print(df)
excel_filename = f'lancome_data_report.xlsx'
with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='rawdata', index=False)
