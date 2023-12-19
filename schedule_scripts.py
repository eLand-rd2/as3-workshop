from scheduler import Scheduler
import time
from datetime import datetime

schedule = Scheduler()


# 印出月報何時被執行的訊息
def monthly_report():
    print("Monthly report executed at", datetime.now())
    # 中間接把資料庫的資料製成報表後的結果並輸出
    print("Monthly report executed successfully at", datetime.now())

# 設定每月的某一天和時間執行排程
day_of_month = 5  # 每月5號
scheduled_time = time(10, 00)  # 早上10點, time()是24小時制

# 定義一個函式，用於在特定的時間點去啟動排程
def schedule_start_monthly_report():
    schedule.every().month.at(f"{scheduled_time.hour}:{scheduled_time.minute}").do(monthly_report)

# 啟動排程
schedule_start_monthly_report()

# 進入無窮迴圈，持續執行排程
while True:
    schedule.run_pending()
    time.sleep(1)