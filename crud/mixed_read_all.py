from sqlalchemy.orm import Session
from datetime import datetime


def get_all_data_with_date(db: Session, start_date, end_date):

    now = datetime.now()  # 取得當前日期和時間
    start_date = now+dateutil.relativedelta.relativedelta(months=-1)  # 取的上個月的日期
    end_date = now

