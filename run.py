#!/usr/bin/env python
import os
import csv

import socrata

def rows():
    for portal in os.listdir('data'):
        for viewid in os.listdir(os.path.join('data', portal, 'views')):
            try:
                row = socrata.load('data', portal, viewid)
            except:
                print portal, viewid
                raise
            if row != None:
                yield row

# metadata = socrata.concat_to_array(rows())

f = open('socrata.csv', 'w')
w = csv.DictWriter(f, rows().next().keys())
for row in rows():
    w.write(row)
f.close()
