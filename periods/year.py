import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

from .period import Period, Granularity
from .week import Week


class Year(Period):

    granularity = Granularity.YEAR

    def __init__(self, year):
        self.start_datetime = datetime(year, 1, 1)
        self.end_datetime = self.start_datetime + relativedelta(years=1)

    def __repr__(self):
        return self.start_datetime.strftime("%Y")

    # When getting weeks for a specified year, we expect to get 1-52 (or 53),
    # not the actual weeks for the datespan (default for Period class),
    # as they may start with for example 52 or end with 1.
    def get_weeks(self, exclude_partial=True):
        end_date = self.get_end_date()
        year = end_date.year
        last_week = end_date.isocalendar()[1]

        if last_week == 1:
            end_date = end_date - relativedelta(days=7)
            last_week = end_date.isocalendar()[1]

        weeks = []
        for c in range(0, last_week):
            week = Week(year, c + 1)
            weeks.append(week)
        return weeks
