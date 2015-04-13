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

    Palal is inspired by choosealicense.com and it uses the same license 
    meta-data. However, while choosealicense.com displays the meta-data for the
    given license, Palal returns the license for the given meta-data.

    If you use Palal, I would love to have your feedback: 

        https://github.com/alixedi/palal

    Now *release* that code!

    :copyright (c) 2015 by Ali Zaidi.
    :license: BSD, see LICENSE for more details.

    ~ * ~
"""
    
import argparse

from license import License, license_loader
from survey import Survey, survey_loader

_desc = 'Answer a few questions to get the best FOSS license for your project.'
parser = argparse.ArgumentParser(description=_desc)

def vector_distance(v1, v2):
    """Given 2 vectors of multiple dimensions, calculate the euclidean 
    distance measure between them."""
    dist = 0
    for dim in v1:
        for x in v1[dim]:
            dd = int(v1[dim][x]) - int(v2[dim][x])
            dist = dist + dd**2
    return dist

def main():
    # parse args
    args = parser.parse_args()
    # load licenses
    lics = license_loader()
    # load survey
    survey = survey_loader()
    # run survey
    survey.run()
    # calculate euclidean distances between license and choice vectors
    dists = []
    for lic in lics:
        d = vector_distance(lic.get_vector(), survey.get_vector())
        dists.append((lic, d))
    # sort distances
    sdists = sorted(dists, key=lambda x: x[1])
    # print results
    print 'According to the given criteria, top 3 FOSS licenses are: '
    for i, sd in enumerate(sdists[:3]):
        lic, dist = sd
        print '(%d) %s' % (i+1, lic.meta['title'])

if __name__ == '__main__':
    main()
