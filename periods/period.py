import os, logging, imp
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from flufl.enum import IntEnum


GLOBAL_START_DATE = datetime(2007,1,1)


class Granularity(IntEnum):
    NONE = 0
    YEAR = 10
    MONTH = 20
    WEEK = 30
    DAY = 40


def granularity_from_string(string):
    if string == 'year':
        return Granularity.YEAR
    elif string == 'month':
        return Granularity.MONTH
    elif string == 'week':
        return Granularity.WEEK
    elif string == 'day':
        return Granularity.DAY
    return None


class Period(object):

    granularity = Granularity.NONE

    def __init__(self, startDate = None, endDate = None):

        if startDate:
            self.startDateTime = datetime.strptime(startDate, '%Y-%m-%d') 
        else:
            self.startDateTime = GLOBAL_START_DATE

        if endDate:
            dateTime = datetime.strptime(endDate, '%Y-%m-%d')
            self.endDateTime = dateTime + relativedelta(days=1)
        else:
            self.endDateTime = datetime.now()


    def __repr__(self):
        return "Start: %s End: %s" % (self.getStartDate().strftime("%Y-%m-%d"), self.getStartDate().strftime("%Y-%m-%d"))


    def getGranularity(self):
        return self.granularity


    def getDateLimits(self):
        return self.startDateTime, self.endDateTime


    def getStartDate(self):
        return self.startDateTime.date()
        

    def getEndDate(self):
        return self.endDateTime.date() - relativedelta(days=1)


    def getCacheKey(self):
        return "%s/%s" % (self.getStartDate(), self.getEndDate())


    def split(self, granularityAfterSplit, excludePartial = True):

        if granularityAfterSplit == Granularity.DAY:
            return self.getDays()

        elif granularityAfterSplit == Granularity.WEEK:
            return self.getWeeks(excludePartial)

        elif granularityAfterSplit == Granularity.MONTH:
            return self.getMonths(excludePartial)

        elif granularityAfterSplit == Granularity.YEAR:
            return self.getYears(excludePartial)

        else:
            raise Exception("Invalid granularity: %s" % granularityAfterSplit)


    def getYears(self, excludePartial):

        from .year import Year

        startDate = self.getStartDate()
        endDate = self.getEndDate()

        if excludePartial:

            if not (startDate.month == 1 and startDate.day == 1): # Startdate not start of year, excluding first year
                startDate = startDate + relativedelta(years=1)

            if not (endDate.month == 12 and endDate.day == 31): # EndDate is not end of year, excluding last year
                endDate = endDate - relativedelta(years=1)

        loopDate = startDate
        years = []

        while loopDate <= endDate:
            year = Year(loopDate.year)
            years.append(year)
            loopDate = loopDate + relativedelta(years=1)

        return years


    def getMonths(self, excludePartial):

        from .month import Month

        startDate = self.getStartDate()
        endDate = self.getEndDate()

        if excludePartial:
        
            if startDate.day != 1: # StartDate is not start of month, exclude first month
                startDate = startDate + relativedelta(months=1)

            endMonthStart = date(endDate.year, endDate.month, 1)
            endMonthEnd = endMonthStart + relativedelta(months=1) - relativedelta(days=1)

            if endDate < endMonthEnd: #EndDate not end of month, exclude last month
                endDate = endDate - relativedelta(months=1)

            if endDate <= startDate:
                raise Exception("Can't get months from period, the granularity is too fine: %s" % self.granularity)

        loopDate = startDate
        months = []
        
        while loopDate <= endDate:
            month = Month(loopDate.year, loopDate.month)
            months.append(month)
            loopDate = loopDate + relativedelta(months=1)

        return months


    def getWeeks(self, excludePartial):

        from .week import Week

        startDate = self.getStartDate()
        startWeekDay = startDate.weekday() 

        endDate = self.getEndDate()
        endWeekDay = endDate.weekday() 

        if excludePartial:
            
            if startWeekDay != 0: # StartDate not start of week, move startDate to next week's start
                startDate = startDate + relativedelta(days=7-startWeekDay)
                
            if endWeekDay != 6: #EndDate not end of week, move endDate to previous week's end
                endDate = endDate - relativedelta(days=endWeekDay)

        else:
            if startWeekDay != 0: # StartDate not start of week, move startDate to start of the week
                startDate = startDate - relativedelta(days=startWeekDay)
                
            if endWeekDay != 6: #EndDate not end of week, move endDate to end of the week
                endDate = endDate + relativedelta(days=6-endWeekDay)

        if endDate <= startDate:
                raise Exception("Can't get weeks from period, the granularity is too fine: %s" % self.granularity)

        weeks = []

        loopDate = startDate
        while loopDate < endDate:
            isoDate = loopDate.isocalendar()
            week = Week(isoDate[0], isoDate[1])
            weeks.append(week)
            loopDate = loopDate + relativedelta(days=7)

        return weeks


    def getDays(self):

        from .day import Day

        loopDate = self.getStartDate()
        days = []

        while loopDate <= self.getEndDate():
            day = Day(loopDate.year, loopDate.month, loopDate.day)
            days.append(day)
            loopDate = loopDate + relativedelta(days=1)

        return days

