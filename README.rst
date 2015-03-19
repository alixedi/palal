======
palal
======

.. image:: https://badge.fury.io/py/palal.png
    :target: http://badge.fury.io/py/palal

.. image:: https://travis-ci.org/alixedi/palal.svg?branch=master
    :target: https://travis-ci.org/alixedi/palal

Pick a license, any license. 

Introduction
------------

Picking an open-source license can be confusing for seasoned developers let along noobs. There are too many choices to begin with. On top of that, there is the vocabulary that reads like English without making any sense.

The situation is unacceptable and it hurts FOSS. 

Palal aims to resolve that. It is a simple CLI utility that asks the user a series of questions In-Plain-English and returns the best possible FOSS license for his/her project.

Palal is inspired by the choosealicense.com and it uses the same license meta-data. However, while choosealicense.com displays the meta-data for the given license, Palal returns the license for the given meta-data.

Installation
------------

Simple. ::

    $ pip install palal

Usage
-----

Choosing a FOSS license is easier than ever before. Just run *palal* and type a number from **1** to **5** for each criterion - specifying how important you feel it is for your project. ::

    $ palal

    What should be forbidden by your license?
    
    Use Trademark (While this may be implicitly true of all licenses, 
    this license explicitly states that you may NOT use the names, logos, 
    or trademarks of contributors.) [0-5] > _

    ...

After the interactive session, you will be presented with the top 3 licenses that match your criteria along with instructions on how to use them. ::

    1) CC0 1.0 Universal [dist=39]

    The Creative Commons CC0 Public Domain Dedication waives copyright interest 
    in any a work you've created and dedicates it to the world-wide public domain.
    Use CC0 to opt out of copyright entirely and ensure your work has the widest 
    reach. As with the Unlicense and typical software licenses, CC0 disclaims 
    warranties. CC0 is very similar to the Unlicense.

    Create a text file (typically named LICENSE or LICENSE.txt) in the root of 
    your source code and copy the text of the CC0 into the file.

    http://creativecommons.org/publicdomain/zero/1.0/

    ...
    
Enjoy!


