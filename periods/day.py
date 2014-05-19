import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .period import Period, Granularity

class Day(Period):

    granularity = Granularity.DAY

    def __init__(self, year, month, day):
        self.startDateTime = datetime(year, month, day)
        self.endDateTime= self.startDateTime + relativedelta(days=1)

    def __repr__(self):
        return self.startDateTime.strftime("%Y-%m-%d")

    def date(self):
        return self.getStartDate()


    

