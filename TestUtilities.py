import unittest
import Utilities

class TestSmoother (unittest.TestCase):
    def test_split_single_colunm(self):
        row, col = Utilities.split_single_colunm(1)
        self.assertEqual(row, 1)
        self.assertEqual(col, 1)
        
        row, col = Utilities.split_single_colunm(2)
        self.assertEqual(row, 1)
        self.assertEqual(col, 2)

        row, col = Utilities.split_single_colunm(3)
        self.assertEqual(row, 2)
        self.assertEqual(col, 2)

        row, col = Utilities.split_single_colunm(6)
        self.assertEqual(row, 2)
        self.assertEqual(col, 3)

        row, col = Utilities.split_single_colunm(7)
        self.assertEqual(row, 3)
        self.assertEqual(col, 3)