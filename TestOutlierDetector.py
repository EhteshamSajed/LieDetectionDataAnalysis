import unittest
import OutlierDetector


class TestOutlierDetector (unittest.TestCase):
    val_list = [1, 2, 3, 4, 5, 6]
    val_list1 = [2, 3, 7, 4, 8, 5, 1, 6]

    def test_max_absolute_change(self):
        result = OutlierDetector.max_absolute_change(self.val_list)
        self.assertEqual(result, [1, 1, 1, 1, 1, 1])
        result = OutlierDetector.max_absolute_change(self.val_list1)
        self.assertEqual(result, [1, 4, 4, 4, 4, 4, 5, 4])
    
    def test_median_absolute_deviation(self):
        result = OutlierDetector.median_absolute_deviation(self.val_list)
        self.assertEqual(result, 0)
        result = OutlierDetector.median_absolute_deviation(self.val_list1)
        self.assertEqual(result, 0)

    def test_get_threshold(self):
        result = OutlierDetector.get_threshold(OutlierDetector.max_absolute_change(self.val_list), OutlierDetector.median_absolute_deviation(self.val_list))
        self.assertEqual(result, 1)
        result = OutlierDetector.get_threshold(OutlierDetector.max_absolute_change(self.val_list1), OutlierDetector.median_absolute_deviation(self.val_list1))
        self.assertEqual(result, 4)

    def test_remove_outliers(self):
        result = OutlierDetector.remove_outliers(self.val_list)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])
        result = OutlierDetector.remove_outliers(self.val_list1)
        self.assertEqual(result, [2, 3, 7, 4, 8, 5, 0, 6])

    def test_relative_position_on_removed_outiler(self):
        result = OutlierDetector.relative_position_on_removed_outiler([2, 3, 7, 0, 8, 5, 0, 6], 4)
        self.assertEqual(result, 3)
        result = OutlierDetector.relative_position_on_removed_outiler([2, 3, 7, 0, 8, 5, 0, 6], 7)
        self.assertEqual(result, 5)
