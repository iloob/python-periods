import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

from .period import Period, Granularity


class HalfYear(Period):

    granularity = Granularity.HALF_YEAR

    def __init__(self, year, half_year):
        self.start_datetime = datetime(year, 1 + (half_year - 1) * 6, 1)
        self.end_datetime = self.start_datetime + relativedelta(months=6)

    def __repr__(self):
        return "%dH%d" % (self.start_datetime.year, self.start_datetime.month / 6 + 1)

