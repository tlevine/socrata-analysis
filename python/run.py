#!/usr/bin/env python
import os
import csv, codecs, cStringIO
from collections import OrderedDict

import socrata

class UnicodeDictWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    @staticmethod
    def encode_if_text(value):
        if isinstance(value, basestring):
            return value.encode('utf-8')
        else:
            return value

    def writerow(self, row):
        self.writer.writerow(OrderedDict(
            [(UnicodeDictWriter.encode_if_text(k), UnicodeDictWriter.encode_if_text(v)) for k,v in row.items()]
        ))
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

    def writeheader(self, *args, **kwargs):
        return self.writer.writeheader(*args, **kwargs)

def check_json():
    'Delete any files that neither empty nor valid JSON.'
    for portal in os.listdir('data'):
        for viewid in os.listdir(os.path.join('data', portal, 'views')):
            try:
                row = socrata.load('data', portal, viewid)
            except ValueError:
                os.remove(os.path.join('data', portal, 'views', viewid))
                print 'Deleted %s/views/%s' % (portal, viewid)

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

def build_ndarray():
    return socrata.concat_to_array(rows())

def build_csv():
    f = open('socrata.csv', 'w')
    w = UnicodeDictWriter(f, rows().next().keys())
    w.writeheader()
    for row in rows():
        w.writerow(row)
    f.close()

def build_geneology():
    CANONICAL_DATASETS = [
        ('explore.data.gov', '5gah-bvex'),
    ]
    result = {}
    for portal, viewid in CANONICAL_DATASETS:
        dataset = socrata.load('data', portal, viewid)
        result[dataset['tableId']] = {
            'source': {'portal': portal, 'id': viewid},
            'datasets': []
        }

    for portal in os.listdir('data'):
        for viewid in os.listdir(os.path.join('data', portal, 'views')):
            row = socrata.load('data', portal, viewid)
            result[row['tableId']]['datasets'].append({
                'portal':        row['portal'],
                'id':            row['id'],
                'name':          row['name'],
                'description':   row['description'],
                'nrow':          row['nrow'],
                'ncol':          row['ncol'],
                'createdAt':     row['createdAt'],
                'viewCount':     row['viewCount'],
                'downloadCount': row['downloadCount'],
            })

    json.dump(result, open('geneology.json', 'w'))
