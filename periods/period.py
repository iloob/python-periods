import os, logging, imp
from datetime import date, datetime, time

from dateutil.relativedelta import relativedelta
from flufl.enum import IntEnum


GLOBAL_START_DATE = datetime(2007, 1, 1)


class Granularity(IntEnum):
    NONE = 0
    YEAR = 10
    HALF_YEAR = 13
    QUARTER = 15
    MONTH = 20
    WEEK = 30
    DAY = 40


def granularity_from_string(string):
    if string == 'year':
        return Granularity.YEAR
    elif string == 'half_year':
        return Granularity.HALF_YEAR
    elif string == 'quarter':
        return Granularity.QUARTER
    elif string == 'month':
        return Granularity.MONTH
    elif string == 'week':
        return Granularity.WEEK
    elif string == 'day':
        return Granularity.DAY
    else:
        return None


class Period(object):

    granularity = Granularity.NONE

    def __init__(self, start_date=None, end_date=None):

        if start_date:
            if isinstance(start_date, date):
                self.start_datetime = datetime.combine(start_date, time())
            else:
                self.start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            self.start_datetime = GLOBAL_START_DATE

        if end_date:
            if isinstance(end_date, date):
                end_datetime = datetime.combine(end_date, time())
            else:
                end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
            self.end_datetime = end_datetime + relativedelta(days=1)
        else:
            self.end_datetime = datetime.now()

    def __repr__(self):
        return "%s - %s" % (self.get_start_date().strftime("%Y-%m-%d"),
                                      self.get_end_date().strftime("%Y-%m-%d"))

    def get_granularity(self):
        return self.granularity

    def get_date_limits(self):
        return self.start_datetime, self.end_datetime

    def get_start_date(self):
        return self.start_datetime.date()

    def get_end_date(self):
        return self.end_datetime.date() - relativedelta(days=1)

    def get_cache_key(self):
        return "%s/%s" % (self.get_start_date(), self.get_end_date())

    def split(self, granularity_after_split, exclude_partial=True):
        """
        Split a period into a given granularity. Optionally include partial
        periods at the start and end of the period.
        """

        if granularity_after_split == Granularity.DAY:
            return self.get_days()

        elif granularity_after_split == Granularity.WEEK:
            return self.get_weeks(exclude_partial)

        elif granularity_after_split == Granularity.MONTH:
            return self.get_months(exclude_partial)

        elif granularity_after_split == Granularity.QUARTER:
            return self.get_quarters(exclude_partial)

        elif granularity_after_split == Granularity.HALF_YEAR:
            return self.get_half_years(exclude_partial)

        elif granularity_after_split == Granularity.YEAR:
            return self.get_years(exclude_partial)

        else:
            raise Exception("Invalid granularity: %s" % granularity_after_split)

    def get_years(self, exclude_partial=True):
        from .year import Year

        start_date = self.get_start_date()
        end_date = self.get_end_date()

        if exclude_partial:
            # Exclude first year if start_date not start of year
            if not (start_date.month == 1 and start_date.day == 1):
                start_date = start_date + relativedelta(years=1)

            # Exclude last year if end_date is not end of year
            if not (end_date.month == 12 and end_date.day == 31):
                end_date = end_date - relativedelta(years=1)

        loop_date = start_date
        years = []

        while loop_date <= end_date:
            year = Year(loop_date.year)
            years.append(year)
            loop_date = loop_date + relativedelta(years=1)

        return years

    def get_quarters(self, exclude_partial=True):
        from .quarter import Quarter

        start_date = self.get_start_date()
        end_date = self.get_end_date()

        loop_date = start_date
        quarters = []

        while loop_date <= end_date:
            quarter = Quarter(loop_date.year, 1 + ((loop_date.month - 1) / 3))
            if not exclude_partial or (start_date <= quarter.get_start_date()
                    and end_date >= quarter.get_end_date()):
                quarters.append(quarter)
            loop_date = loop_date + relativedelta(months=3)

        return quarters

    def get_half_years(self, exclude_partial=True):
        from .halfyear import HalfYear

        start_date = self.get_start_date()
        end_date = self.get_end_date()

        loop_date = start_date
        half_years = []

        while loop_date <= end_date:
            half_year = HalfYear(loop_date.year, 1 + ((loop_date.month - 1) / 6))
            if not exclude_partial or (start_date <= half_year.get_start_date()
                    and end_date >= half_year.get_end_date()):
                half_years.append(half_year)
            loop_date = loop_date + relativedelta(months=6)

        return half_years

    def get_months(self, exclude_partial=True):
        from .month import Month

        start_date = self.get_start_date()
        end_date = self.get_end_date()

        if exclude_partial:

            # Exclude first month if start_date is not start of month
            if start_date.day != 1:
                start_date = start_date + relativedelta(months=1)

            end_month_start = date(end_date.year, end_date.month, 1)
            end_month_end = end_month_start + relativedelta(months=1) - relativedelta(days=1)

            # Exclude last month if end_date is not end of month
            if end_date < end_month_end:
                end_date = end_month_end - relativedelta(months=1)

        loop_date = start_date
        months = []

        while loop_date <= end_date:
            month = Month(loop_date.year, loop_date.month)
            months.append(month)
            loop_date = loop_date + relativedelta(months=1)

        return months

    def get_weeks(self, exclude_partial=True):
        from .week import Week

        start_date = self.get_start_date()
        start_week_day = start_date.weekday()

        end_date = self.get_end_date()
        end_week_day = end_date.weekday()

        if exclude_partial:

            # If start_date is not start of week, move start_date to next week's start
            if start_week_day != 0:
                start_date = start_date + relativedelta(days=7-start_week_day)

            # If end_date is not end of week, move end_date to previous week's end
            if end_week_day != 6:
                end_date = end_date - relativedelta(days=end_week_day)

        else:
            # If start_date not start of week, move start_date to start of the week
            if start_week_day != 0:
                start_date = start_date - relativedelta(days=start_week_day)

            # If end_date not end of week, move end_date to end of the week
            if end_week_day != 6:
                end_date = end_date + relativedelta(days=6-end_week_day)

        weeks = []

        loop_date = start_date
        while loop_date < end_date:
            iso_date = loop_date.isocalendar()
            week = Week(iso_date[0], iso_date[1])
            weeks.append(week)
            loop_date = loop_date + relativedelta(days=7)

        return weeks

    def get_days(self):
        from .day import Day

        loop_date = self.get_start_date()
        days = []

        while loop_date <= self.get_end_date():
            day = Day(loop_date.year, loop_date.month, loop_date.day)
            days.append(day)
            loop_date = loop_date + relativedelta(days=1)

        return days
