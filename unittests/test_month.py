import unittest
from datetime import date
from periods import *


class MonthTest(unittest.TestCase):

    def testGetMonthStartAndEnd(self):

        period = Month(2009, 7)
        start_date = period.get_start_date()
        end_date = period.get_end_date()

        self.assertEqual(date(2009, 7, 1), start_date)
        self.assertEqual(date(2009, 7, 31), end_date)

        # Leap year
        period = Month(2012, 2)
        start_date = period.get_start_date()
        end_date = period.get_end_date()

        self.assertEqual(date(2012, 2, 1), start_date)
        self.assertEqual(date(2012, 2, 29), end_date)
