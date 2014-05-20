import unittest
from datetime import date
from periods import *


class DayTest(unittest.TestCase):

    def testGetDayStartAndEnd(self):
        period = Day(2009, 7, 1)
        start_date = period.get_start_date()
        end_date = period.get_end_date()

        self.assertEqual(date(2009, 7, 1), start_date)
        self.assertEqual(date(2009, 7, 1), end_date)
