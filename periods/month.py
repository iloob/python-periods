import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .period import Period, Granularity

class Month(Period):

    granularity = Granularity.MONTH

    def __init__(self, year, month):
        self.startDateTime = datetime(year, month, 1)
        self.endDateTime = self.startDateTime + relativedelta(months=1)

    def __repr__(self):
        return self.startDateTime.strftime("%Y-%m")
