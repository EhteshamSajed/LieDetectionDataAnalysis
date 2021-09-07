import unittest
import Analysis
import json


class TestAnalysis (unittest.TestCase):   
    
    def test_assess_participants_answer(self):
        data = json.load(open("ExpData/M33_4.dat"))
        # free
        pupil_data_trial = data['trials'][0]['pupilDataTrials'][0]
        result = Analysis.assess_participants_answer(pupil_data_trial, 'Any')
        self.assertEqual(result, True)
        # free
        pupil_data_trial = data['trials'][0]['pupilDataTrials'][1]
        result = Analysis.assess_participants_answer(pupil_data_trial, 'True')
        self.assertEqual(result, True)
        # free
        pupil_data_trial = data['trials'][0]['pupilDataTrials'][2]
        result = Analysis.assess_participants_answer(pupil_data_trial, 'True')
        self.assertEqual(result, True)
        # lie
        pupil_data_trial = data['trials'][0]['pupilDataTrials'][3]
        result = Analysis.assess_participants_answer(pupil_data_trial, 'True')
        self.assertEqual(result, False)
        # lie
        pupil_data_trial = data['trials'][0]['pupilDataTrials'][5]
        result = Analysis.assess_participants_answer(pupil_data_trial, 'True')
        self.assertEqual(result, True)
