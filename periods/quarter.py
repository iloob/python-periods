import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

from .period import Period, Granularity


class Quarter(Period):

    granularity = Granularity.QUARTER

    def __init__(self, year, quarter):
        self.start_datetime = datetime(year, 1 + (quarter - 1) * 3, 1)
        self.end_datetime = self.start_datetime + relativedelta(months=3)

    def __repr__(self):
        return "%dQ%d" % (self.start_datetime.year, self.start_datetime.month / 3 + 1)

