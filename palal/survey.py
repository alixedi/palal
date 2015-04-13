# -*- coding: utf-8 -*-

"""
    palal.survey
    ------------

    This file is home the Survey class.

    A Survey class must start with some questions that are arranged into 
    categories.

    It has functions that ask the questions nicely.

    And finally, if all goes well, it has answers.

    :copyright: (c) 2015 by Ali Zaidi.
    :license: BSD, see LICENSE for more details.
"""

import os
import yaml
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
SUR_DIR = os.path.join(DIR, '_data')
SUR_FILE = 'rules.yml'

def _stdin_(p):
    """Takes input from user. Works for Python 2 and 3."""
    _v = sys.version[0]
    return input(p) if _v is '3' else raw_input(p)


class Survey(object):
    """Questions. How to ask them. Answers."""

    def __init__(self, survey_text, choices=None):
        """Parse the YAML for questions."""
        self.survey = yaml.load(survey_text)
        self.choices = choices or self.get_choices()
        self.qcount = 1
        # calcuate total questions
        self.qtotal = 0
        for sec in self.survey.values():
            self.qtotal += len(sec)

    def get_choices(self):
        """Get sane defaults for choices."""
        return ['No', 'Maybe', 'Yes']

    def format_choices(self):
        """Return the choices in string form."""
        ce = enumerate(self.choices)
        f = lambda i, c: '%s (%d)' % (c, i+1)
        # apply formatter and append help token
        toks = [f(i,c) for i, c in ce] + ['Help (?)']
        return ' '.join(toks)

    def is_answer_valid(self, ans):
        """Validate user's answer against available choices."""
        return ans in [str(i+1) for i in range(len(self.choices))]

    def run_question(self, question, input_func=_stdin_):
        """Run the given question."""
        qi = '[%d/%d] ' % (self.qcount, self.qtotal)
        print('%s %s:' % (qi, question['label']))
        while True:
            # ask for user input until we get a valid one
            ans = input_func('%s > ' % self.format_choices())
            if self.is_answer_valid(ans): 
                question['answer'] = int(ans)
                break
            else:
                if ans is '?': print(question['description'])
                else: print('Invalid answer.')
        self.qcount += 1

    def run_section(self, name, input_func=_stdin_):
        """Run the given section."""
        print('\nStuff %s by the license:\n' % name)
        section = self.survey[name]
        for question in section:
            self.run_question(question, input_func)

    def run(self, input_func=_stdin_):
        """Run the sections."""
        # reset question count
        self.qcount = 1
        for section_name in self.survey:
            self.run_section(section_name, input_func)

    def get_vector(self):
        """Return the vector for this survey."""
        vec = {}
        for dim in ['forbidden', 'required', 'permitted']:
            if self.survey[dim] is None:
                continue
            dim_vec = map(lambda x: (x['tag'], x['answer']), 
                          self.survey[dim])
            vec[dim] = dict(dim_vec)
        return vec



def survey_loader(sur_dir=SUR_DIR, sur_file=SUR_FILE):
    """Loads up the given survey in the given dir."""
    survey_path = os.path.join(sur_dir, sur_file)
    survey = None
    with open(survey_path) as survey_file:
        survey = Survey(survey_file.read())
    return survey