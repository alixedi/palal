import os
import unittest
import random

from palal import survey


def _mockin_():
    return 


class TestSurvey(unittest.TestCase):
    
    def setUp(self):
        """Set-up our survey."""
        survey_path = os.path.join(survey.SUR_DIR, 'rules.yml')
        with open(survey_path) as survey_file:
            self.survey = survey.Survey(survey_file.read())

    def test_survey(self):
        """Fixed answer."""
        fix_ans = lambda x: '1'
        self.survey.run(input_func=fix_ans)
        for sec_name in self.survey.survey:
        	for question in self.survey.survey[sec_name]:
        		assert question['answer'] == 1