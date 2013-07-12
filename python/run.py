#!/usr/bin/env python
import os
import json
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

def build_tables():
    result = {}
    for portal in os.listdir('data'):
        for viewid in os.listdir(os.path.join('data', portal, 'views')):
            handle = open(os.path.join('data', portal, 'views', viewid), 'r')
            dataset = json.load(handle)
            handle.close()
            if dataset == None:
                continue

            if dataset['tableId'] not in result:
                result[dataset['tableId']] = {
                    'source': {},
                    'datasets': {},
                }

            result[dataset['tableId']]['datasets'][dataset['id']] = {
                'portal':        dataset['portal'],
                'id':            dataset['id'],
                'name':          dataset['name'],
                'description':   dataset['description'],
                'nrow':          dataset['nrow'],
                'ncol':          dataset['ncol'],
                'createdAt':     dataset['createdAt'],
                'viewCount':     dataset['viewCount'],
                'downloadCount': dataset['downloadCount'],
                'modifyingViewUid': dataset.get('modifyingViewUid'),
            }

            if 'viewFilters' in dataset:
                result[dataset['tableId']]['source'] = result[dataset['tableId']]['datasets'][dataset['id']]

    for tableId in result:
        result[tableId]['datasets'] = result[tableId]['datasets'].values()

    try:
        os.mkdir('geneology')
    except OSError:
        pass
    for tableId, tableData in result.items():
        json.dump(tableData, open(os.path.join('geneology', tableId + '.json'), 'w'))
    json.dump(result.keys(), open(os.path.join('geneology', 'index.json'), 'w'))
