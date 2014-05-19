import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

from .period import Period, Granularity


class Month(Period):

    granularity = Granularity.MONTH

    def __init__(self, year, month):
        self.start_datetime = datetime(year, month, 1)
        self.end_datetime = self.start_datetime + relativedelta(months=1)

    def __repr__(self):
        return self.start_datetime.strftime("%Y-%m")
