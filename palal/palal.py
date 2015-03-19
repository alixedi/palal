# -*- coding: utf-8 -*-

"""
    Palal - Pick A License, Any License!
    ------------------------------------

    Picking an open-source license can be confusing for seasoned developers
    let along noobs. There are too many choices to begin with. On top of that,
    there is the vocabulary that reads like English without making any sense.

    The situation is unacceptable and it hurts FOSS. 

    Palal aims to resolve that. It is a simple CLI utility that asks the user
    a series of questions In-Plain-English and returns the best possible FOSS
    license for his/her project.

    Palal is inspired by the choosealicense.com and it uses the same license 
    meta-data. However, while choosealicense.com displays the meta-data for the
    given license, Palal returns the license for the given meta-data.

    If you use Palal, I would love to have your feedback: 

        https://github.com/alixedi/palal

    Now *release* that code!

    :copyright (c) 2015 by Ali Zaidi.
    :license: BSD, see LICENSE for more details.

    ~ * ~
"""
    
import os
import sys
import yaml
import argparse

# Constants
DIR = os.path.dirname(os.path.realpath(__file__))
DATA = os.path.join(DIR, '_data')
RULES = os.path.join(DATA, 'rules.yml')
LICENSES = os.path.join(DIR, '_licenses')
YAML_SEP = '---'

_desc = 'Answer a few questions to get the best FOSS license for your project.'
parser = argparse.ArgumentParser(description=_desc)

# Prettyprints
def printh2(s):
    print('\n' + s)

def printh1(s):
    print('\n' + s + '\n')

# Wrapper for raw_input
def uinput(p):
    _v = sys.version[0]
    return input(p) if _v is '3' else raw_input(p)

# Utility functions
def load_rules():
    """Load rules - collection of tags, labels and descriptions."""
    s = open(os.path.join(DATA, RULES))
    return yaml.load(s)


def extract_yaml(txt, sep):
    """Extracts YAML and returns it along with leftover."""
    tks = txt.split(sep)
    return tks[1], ''.join(tks[2:])


def process_lic(name):
    """Process a single license file."""
    path = os.path.join(LICENSES, name)
    with open(path) as lic:
        y, md = extract_yaml(lic.read(), YAML_SEP)
        return (name, (yaml.load(y), md))


def load_licenses():
    """Load all the license files and their metadata."""
    lics = [l for l in os.listdir(LICENSES)]
    data = map(process_lic, lics)
    return dict(data)


def get_choice(rule):
    """Ask question, get choice."""
    tag = rule['tag']
    label = rule['label']
    description = rule['description']
    ch = uinput('%s (%s) [1-5] > ' % (label, description))
    if ch in ['1', '2', '3', '4', '5']:
        return tag, ch

    printh2('Please enter a number between 1 and 5!')
    return get_choice(rule)


def get_choice_vector(rules):
    """Ask questions get choices."""
    return dict(map(get_choice, rules))


def get_license_vector(lic):
    """Return pseudo-choice vector given license."""
    data, _ = lic
    vec = {}
    for dim in ['forbidden', 'required', 'permitted']:
        if data[dim] is None:
            continue
        dim_vec = map(lambda x: (x,5), data[dim])
        vec[dim] = dict(dim_vec)
    return vec


def vector_distance(v, _v):
    dist = 0
    for dim in v:
        for x in v[dim]:
            dd = int(v[dim][x]) - int(_v[dim][x])
            dist = dist + dd**2
    return dist

def dget(d, k):
    return d[k] if k in d else ''


def main():
    # parse args
    args = parser.parse_args()
    # load everything
    lics = load_licenses()
    rules = load_rules()
    ch_vectors = {}
    lic_vectors = {}
    dists = []

    # get user choices
    for rule in rules:
        text = 'What should be %s by your license?' % rule 
        printh1(text)
        ch_vectors[rule] = get_choice_vector(rules[rule])

    # get license stuff
    for lic in lics:
        lic_vectors[lic] = get_license_vector(lics[lic])

    # calculate distance
    for lic in lics:
        d = vector_distance(lic_vectors[lic], ch_vectors)
        dists.append((lic, d))

    # sort distances
    sdists = sorted(dists, key=lambda x: x[1])

    # print results
    printh2('According to the given criteria, top 3 FOSS licenses are: ')
    for i, sd in enumerate(sdists[:3]):
        lic, dist = sd
        data, txt = lics[lic]
        printh2('%d) %s [dist=%s]' % (i+1, dget(data, 'title'), d))
        printh2(dget(data, 'description'))
        printh2(dget(data, 'how'))
        printh2(dget(data, 'source'))

if __name__ == '__main__':
    main()
