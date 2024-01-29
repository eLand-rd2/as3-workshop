from scheduler import Scheduler
import time
import datetime as dt

import settings

schedule = Scheduler()


# load class from path string
def load_class(full_path):
    module = '.'.join(full_path.split('.')[:-1])
    cls = full_path.split('.')[-1]
    mod = __import__(module, fromlist=[cls])
    return getattr(mod, cls)


def run_spider_task():
    # 從settings拿target_urls
    # 藉由CLICK取得爬文間隔、停止時間的參數
    # 建立schedule 依參數執行爬文任務
    targets = settings.spider_target
    for target in targets:
        run_spider(target)


def run_spider(target):
    # 利用target_urls裡的爬文模組與目標網址取得爬文結果
    # 利用crud函式將結果寫進資料庫
    # 印出月報何時被執行的訊息
    spider_cls_path = target['spider_class']
    spider_cls = load_class(spider_cls_path)
    urls = target['urls']
    print("Spider executed at", dt.datetime.now())
    print(f"{spider_cls_path=}")
    print(f"{urls=}")


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

    run_spider_task()
    # # 設定每月的某一天和時間執行排程
    # scheduled_day = 5  # 每月5號
    # scheduled_hour = 10  # 早上10點, time()是24小時制
    #
    # # 啟動排程
    # schedule_start_monthly_report(scheduled_day, scheduled_hour)
    #
    # # 進入無窮迴圈，持續執行排程
    # while True:
    #     schedule.exec_jobs()
    #     time.sleep(1)
