import unittest
from datetime import date
from periods import *


class GranularityTest(unittest.TestCase):

    def testGranularityTypes(self):
        self.assertTrue(Granularity.YEAR < Granularity.MONTH)
        self.assertTrue(Granularity.MONTH < Granularity.WEEK)
        self.assertTrue(Granularity.WEEK < Granularity.DAY)


class PeriodTest(unittest.TestCase):

    def testSplitPeriodIntoMonths(self):

        period = Year(2009)

        months = period.split(Granularity.MONTH)
        self.assertEqual(12, len(months))
        sample = months[6]
        self.assertEqual(date(2009, 7, 1), sample.get_start_date())
        self.assertEqual(date(2009, 7, 31), sample.get_end_date())

        period = Month(2009, 7)

        months = period.split(Granularity.MONTH)
        self.assertEqual(1, len(months))
        sample = months[0]
        self.assertEqual(date(2009, 7, 1), sample.get_start_date())
        self.assertEqual(date(2009, 7, 31), sample.get_end_date())


    def testSplitPeriodIntoMonthsIncludePartial(self):

        period = Period('2012-06-15', '2014-12-15')

        months = period.split(Granularity.MONTH, exclude_partial = False)
        self.assertEqual(31, len(months))
        sample = months[2]
        self.assertEqual(date(2012, 8, 1), sample.get_start_date())
        self.assertEqual(date(2012, 8, 31), sample.get_end_date())


    def testSplitPeriodIntoMonthsExcludePartial(self):

        period = Period('2012-06-15', '2014-12-15')

        months = period.split(Granularity.MONTH, exclude_partial = True)
        self.assertEqual(29, len(months))
        sample = months[2]
        self.assertEqual(date(2012, 9, 1), sample.get_start_date())
        self.assertEqual(date(2012, 9, 30), sample.get_end_date())


    def testSplitPeriodIntoWeeks(self):

        period = Period('2013-06-01', '2014-12-31')

        weeks = period.split(Granularity.WEEK, exclude_partial = True)
        self.assertEquals(82, len(weeks)) 
        self.assertEqual(date(2013, 6, 3), weeks[0].get_start_date())
        self.assertEqual(date(2014, 12, 28), weeks[81].get_end_date())

        weeks = period.split(Granularity.WEEK, exclude_partial = False)
        self.assertEquals(84, len(weeks))
        self.assertEqual(date(2013, 5, 27), weeks[0].get_start_date())
        self.assertEqual(date(2015, 1, 4), weeks[83].get_end_date())

        period = Week(2014, 7)
        weeks = period.split(Granularity.WEEK)
        self.assertEquals(1, len(weeks))
        self.assertEqual(date(2014, 2, 10), weeks[0].get_start_date())


    def testSplitPeriodIntoDays(self):

        period = Year(2013)
        days = period.split(Granularity.DAY)
        self.assertEqual(365, len(days))

        period = Period('2013-06-01', '2013-12-31')

        days = period.split(Granularity.DAY)
        self.assertEquals(214, len(days))
        self.assertEqual(date(2013, 6, 1), days[0].date())
        self.assertEqual(date(2013, 12, 31), days[213].date())


        period = Week(2014, 7)
        days = period.split(Granularity.DAY)
        self.assertEquals(7, len(days))
        #self.assertEqual(date(2014, 2, 10), weeks[0].get_start_date())

        period = Day(2009, 7, 1)
        days = period.split(Granularity.DAY)
        self.assertEquals(1, len(days))
        #self.assertEqual(date(2014, 2, 10), weeks[0].get_start_date())
