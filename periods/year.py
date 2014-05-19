import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .period import Period, Granularity

class Year(Period):

    granularity = Granularity.YEAR

    def __init__(self, year):
        self.startDateTime = datetime(year, 1, 1)
        self.endDateTime = self.startDateTime + relativedelta(years=1)

    def __repr__(self):
        return self.startDateTime.strftime("%Y")

    # When getting weeks for a specified year, we expect to get 1-52 (or 53), not the actual weeks for the datespan (default for Period class), 
    # as they may start with for example 52 or end with 1.
    def getWeeks(self, excludePartial):
        
        from models.dateutils import Week

        endDate = self.getEndDate()
        year = endDate.year
        lastWeek = endDate.isocalendar()[1]

        if lastWeek == 1:
            endDate = endDate - relativedelta(days=7)
            lastWeek = endDate.isocalendar()[1]

        weeks = []
        for c in range(0, lastWeek):
            week = Week(year, c + 1)
            weeks.append(week)
        return weeks
