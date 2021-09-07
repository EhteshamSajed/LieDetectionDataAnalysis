import unittest
import Smoother

class TestSmoother (unittest.TestCase):
    val_list = [1, 2, 3, 4, 5, 6]
    val_list1 = [2, 3, 7, 4, 8, 5, 0, 6]

    def test_smooth(self):
        result = Smoother.smooth(self.val_list, 3, False)
        self.assertEqual(result, [1, 2, 3, 3, 4, 5])
        result = Smoother.smooth(self.val_list1, 3, True)
        self.assertEqual(result, [2, 3, 7, 4, 8, 5, 0, 6])
        result = Smoother.smooth(self.val_list1, 3, False)
        self.assertEqual(result, [2, 3, 7, 4, 8, 5, 0, 6])