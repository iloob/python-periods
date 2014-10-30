import unittest
from datetime import date
from periods import *


class QuerterTest(unittest.TestCase):

    def testGetQuerterStartAndEnd(self):

        period = Quarter(2009, 1)
        start_date = period.get_start_date()
        end_date = period.get_end_date()

        self.assertEqual(date(2009, 01, 01), start_date)
        self.assertEqual(date(2009, 03, 31), end_date)

        period = Quarter(2011, 2)
        start_date = period.get_start_date()
        end_date = period.get_end_date()

        self.assertEqual(date(2011, 04, 01), start_date)
        self.assertEqual(date(2011, 06, 30), end_date)

        period = Quarter(2010, 3)
        start_date = period.get_start_date()
        end_date = period.get_end_date()

        self.assertEqual(date(2010, 07, 01), start_date)
        self.assertEqual(date(2010, 9, 30), end_date)

        period = Quarter(2010, 4)
        start_date = period.get_start_date()
        end_date = period.get_end_date()

        self.assertEqual(date(2010, 10, 01), start_date)
        self.assertEqual(date(2010, 12, 31), end_date)


