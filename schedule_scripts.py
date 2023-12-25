from scheduler import Scheduler
import time
import datetime as dt

schedule = Scheduler()


# 印出月報何時被執行的訊息
def monthly_report(day):
    today = dt.datetime.now()
    if not today.day == day:
        return
    print("Monthly report executed at", today)
    # 中間接把資料庫的資料製成報表後的結果並輸出
    print("Monthly report executed successfully at", today)


def schedule_start_monthly_report(day, hour):
    schedule.daily(dt.time(hour=hour), monthly_report, kwargs={
        'day': day
    })


if __name__ == '__main__':

    # 設定每月的某一天和時間執行排程
    scheduled_day = 5  # 每月5號
    scheduled_hour = 10  # 早上10點, time()是24小時制

    # 啟動排程
    schedule_start_monthly_report(scheduled_day, scheduled_hour)

    # 進入無窮迴圈，持續執行排程
    while True:
        schedule.exec_jobs()
        time.sleep(1)
