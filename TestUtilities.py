import unittest
import Utilities
import json

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

    def test_average_within_condition (self):
        condition_index=3
        count = 2
        data = json.load(open("testFiles/sampleJson.dat"))
        extracted = Utilities.extract_data(
            data=data, search_from=0, count=count, feedbackCondition=0, 
            participantAnswer=0, condition_index=condition_index, baseline_source=Utilities.Baseline_Source.preceding_trial)
        average_trend = Utilities.average_within_condition(
            extracted, Utilities.Trial_Data.smoothed.name, Utilities.CONDITIONS[condition_index])
        average_response_time = int (average_trend["average_elapsed_ticks_to_answer"]/10000000 * 60)
        self.assertEqual(220, average_response_time)

    def test_assess_participants_answer(self):
        data = json.load(open("testFiles/sampleJson.dat"))
        pupilDataTrial = data['trials'][0]['pupilDataTrials'][1]    # free_true
        self.assertEqual(True, Utilities.assess_participants_answer(pupilDataTrial, Utilities.ANSWERES[1]))

        pupilDataTrial = data['trials'][0]['pupilDataTrials'][19]    # free_false
        self.assertEqual(True, Utilities.assess_participants_answer(pupilDataTrial, Utilities.ANSWERES[2]))
