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

import yaml
import sys


def ui(p):
    """Takes input from user. Works for Python 2 and 3."""
    _v = sys.version[0]
    return input(p) if _v is '3' else raw_input(p)


class Survey(object):
    """Questions. How to ask them. Answers."""

    def __init__(self, survey_text, choices=None):
        """Parse the YAML for questions."""
        self.survey = yaml.load(survey_text)
        self.choices = choices or self.get_choices()

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
        return ans in [i+1 for i in range(len(self.choices))]

    def run(self):
        """Run the survey. Ask questions. Validate answers. Store them."""
        for secname in self.survey:
            print('\nStuff %s by the license:\n' % secname)
            sec = self.survey[secname]
            # number of questions in section
            t = len(sec) + 1
            # run through questions
            for i, q in enumerate(sec):
                qi = '[%d/%d] ' % (i+1, t)
                print('%s %s:' % (qi, q['label']))
                while True:
                    ans = ui('%s > ' % self.format_choices())
                    if self.is_answer_valid(ans): 
                        q['answer'] = ans
                        break
                    if ans is '?': print(q['description'])
                    else: print('Invalid answer.')

