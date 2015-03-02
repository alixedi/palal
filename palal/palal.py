import os
import yaml

import sys
if sys.version[0]=="3": raw_input=input


DIR = os.path.dirname(os.path.realpath(__file__))
DATA = os.path.join(DIR, '_data')
RULES = os.path.join(DATA, 'rules.yml')
LICENSES = os.path.join(DIR, '_licenses')
YAML_SEP = '---'


# Prettyprint utilities
def print1(s):
    print('')
    print(s)

def print2(s):
    print('')
    print(s)
    print('')


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
    ch = raw_input('%s (%s) [1-5] > ' % (label, description))
    if ch in ['1', '2', '3', '4', '5']:
        return tag, ch

    print1('Please enter a number between 1 and 5!')
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
    # load everything
    lics = load_licenses()
    rules = load_rules()
    ch_vectors = {}
    lic_vectors = {}
    dists = []

    # get user choices
    for rule in rules:
        text = 'What should be %s by your license?' % rule 
        print2(text)
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
    print1('According to the given criteria, top 3 FOSS licenses are: ')
    for i, sd in enumerate(sdists[:3]):
        lic, dist = sd
        data, txt = lics[lic]
        print1('%d) %s [dist=%s]' % (i+1, dget(data, 'title'), d))
        print1(dget(data, 'description'))
        print1(dget(data, 'how'))
        print1(dget(data, 'source'))

if __name__ == '__main__':
    main()
