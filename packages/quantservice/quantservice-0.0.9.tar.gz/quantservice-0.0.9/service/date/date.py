import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class Date:
    @staticmethod
    def generate_month(start: str, end: str, interval: int):
        month_list = []
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")

        tmp_date = start_date
        while tmp_date != end_date:
            month_list.append(tmp_date.strftime("%Y-%m-%d"))
            tmp_date = tmp_date + relativedelta(months=interval)
        month_list.append(end_date.strftime("%Y-%m-%d"))
        return month_list

    @staticmethod
    def generate_day(start: str, end: str, interval: int):
        day_list = []
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")

        tmp_date = start_date
        while tmp_date != end_date:
            day_list.append(tmp_date.strftime("%Y-%m-%d"))
            tmp_date = tmp_date + timedelta(days=interval)
        day_list.append(end_date.strftime("%Y-%m-%d"))
        return day_list

