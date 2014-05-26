import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

from .period import Period, Granularity


class Day(Period):

    granularity = Granularity.DAY

    def __init__(self, year, month, day):
        self.start_datetime = datetime(year, month, day)
        self.end_datetime = self.start_datetime + relativedelta(days=1)

    def __repr__(self):
        return self.start_datetime.strftime("%Y-%m-%d")

    def date(self):
        return self.get_start_date()
