#!/usr/bin/env python
import os

import socrata

def rows():
    for portal in os.listdir('data')[1:3]:
        for viewid in os.listdir(os.path.join('data', portal, 'views'))[:8]:
            row = socrata.load('data', portal, viewid)
            if row != None:
                yield row

metadata = socrata.concat_to_array(rows())
