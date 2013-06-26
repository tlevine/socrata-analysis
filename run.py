#!/usr/bin/env python
import os

import socrata

def rows():
    for portal in os.listdir('data'):
        for viewid in os.listdir(os.path.join('data', portal, 'views')):
            print portal,viewid
            yield socrata.load('data', portal, viewid)
            break

metadata = socrata.concat_to_array(rows())
