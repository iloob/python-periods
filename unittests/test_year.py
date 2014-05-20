import unittest
from datetime import date
from periods import *


class YearTest(unittest.TestCase):
    
    def testGetYearStartAndEnd(self):

        period = Year(2009)
        start_date = period.get_start_date()
        end_date = period.get_end_date()

        self.assertEqual(date(2009, 1, 1), start_date)
        self.assertEqual(date(2009, 12, 31), end_date)


    def testSplitYearIntoWeeks(self):

        year = Year(2009)
        weeks = year.split(Granularity.WEEK)
        self.assertEqual(53, len(weeks))
        self.assertEqual(date(2008, 12, 29), weeks[0].get_start_date())
        self.assertEqual(date(2010, 1, 3), weeks[52].get_end_date())

        year = Year(2013)
        weeks = year.split(Granularity.WEEK)
        self.assertEqual(52, len(weeks))
