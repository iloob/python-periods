import unittest
from datetime import date
from periods import *


class WeekTest(unittest.TestCase):

    def testGetWeekStartAndEnd(self):

        period = Week(2009, 53)
        start_date = period.get_start_date()
        end_date = period.get_end_date()

        self.assertEqual(date(2009, 12, 28), start_date)
        self.assertEqual(date(2010, 01, 03), end_date)

        period = Week(2014, 1)
        start_date = period.get_start_date()
        end_date = period.get_end_date()

        self.assertEqual(date(2013, 12, 30), start_date)
        self.assertEqual(date(2014, 1, 5), end_date)

        period = Week(2014, 8)
        start_date = period.get_start_date()
        end_date = period.get_end_date()

        self.assertEqual(date(2014, 2, 17), start_date)
        self.assertEqual(date(2014, 2, 23), end_date)
