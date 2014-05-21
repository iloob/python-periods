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
        start_date = IsoWeek(year, week).monday()
        self.start_datetime = datetime.combine(start_date, datetime.min.time())
        self.end_datetime = self.start_datetime + relativedelta(days=7)

    def __repr__(self):
        if self.get_start_date().year != self.get_end_date().year:
            if self.week == 1:
                return "%sW1" % self.get_end_date().year
            elif self.week > 51:
                return "%sW%s" % (self.get_start_date().year,
                                  self.get_start_date().isocalendar()[1])

        return "%sW%s" % (self.get_start_date().year,
                          self.get_start_date().isocalendar()[1])
