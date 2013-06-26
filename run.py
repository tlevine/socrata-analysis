#!/usr/bin/env python
import os

import socrata

def rows():
    for portal in os.listdir('data'):
        for viewid in os.listdir(os.path.join('data', portal, 'views'))[-100:]:
            try:
                row = socrata.load('data', portal, viewid)
            except:
                print portal, viewid
                raise
            if row != None:
                yield row

metadata = socrata.concat_to_array(rows())
