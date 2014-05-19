import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week as IsoWeek
from .period import Period, Granularity

class Week(Period):

    granularity = Granularity.WEEK

    def __init__(self, year, week):
        self.year = year
        self.week = week
        startDate = IsoWeek(year, week).monday()
        self.startDateTime = datetime.combine(startDate, datetime.min.time())
        self.endDateTime = self.startDateTime + relativedelta(days=7)


    def __repr__(self):
        if self.getStartDate().year != self.getEndDate().year:
            if self.week == 1:
                return "%sW1" % self.getEndDate().year
            elif self.week > 51:
                return "%sW%s" % (self.getStartDate().year, self.getStartDate().isocalendar()[1])

        return "%sW%s" % (self.getStartDate().year, self.getStartDate().isocalendar()[1])
