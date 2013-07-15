#!/usr/bin/env python
import os
import json
import csv, codecs, cStringIO
from collections import OrderedDict

from dumptruck import DumpTruck

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
    for portal in ['data.cityofnewyork.us']:# os.listdir('data'):
        for viewid in os.listdir(os.path.join('data', portal, 'views')):
            dataset_flat = socrata.load('data', portal, viewid)
            if dataset_flat == None:
                continue
            handle = open(os.path.join('data', portal, 'views', viewid), 'r')
            dataset = json.load(handle)
            handle.close()

            if dataset['tableId'] not in result:
                result[dataset['tableId']] = {
                    'source': {},
                    'datasets': {},
                }

            dataset_info = {
                'portal':        portal,
                'id':            dataset_flat['id'],
                'name':          dataset_flat['name'],
                'description':   dataset_flat['description'],
                'nrow':          dataset_flat['nrow'],
                'ncol':          dataset_flat['ncol'],
                'createdAt':     dataset_flat['createdAt'],
                'viewCount':     dataset_flat['viewCount'],
                'downloadCount': dataset_flat['downloadCount'],
                'modifyingViewUid': dataset.get('modifyingViewUid'),
                'has_viewFilters': 'viewFilters' in dataset,
            }

            result[dataset['tableId']]['datasets'][dataset['id']] = dataset_info
            if 'viewFilters' not in dataset:
                result[dataset['tableId']]['source'] = dataset_info

    for tableId in result:
        result[tableId]['datasets'] = result[tableId]['datasets'].values()

    try:
        os.mkdir('geneology')
    except OSError:
        pass


    json.dump(result[908693], open(os.path.join('geneology', '908693.json'), 'w'))

#   for tableId, tableData in result.items():
#       json.dump(tableData, open(os.path.join('geneology', tableId + '.json'), 'w'))
#   json.dump(result.keys(), open(os.path.join('geneology', 'index.json'), 'w'))


def _dataset_table_info(portal, viewid):
    dataset_flat = socrata.load('data', portal, viewid)
    if dataset_flat == None:
        return None
    handle = open(os.path.join('data', portal, 'views', viewid), 'r')
    dataset = json.load(handle)
    handle.close()
    dataset_info = {
        'portal':        portal,
        'id':            dataset_flat['id'],
        'name':          dataset_flat['name'],
        'description':   dataset_flat['description'],
        'tableId':       dataset['tableId'],
        'nrow':          dataset_flat['nrow'],
        'ncol':          dataset_flat['ncol'],
        'createdAt':     dataset_flat['createdAt'],
        'viewCount':     dataset_flat['viewCount'],
        'downloadCount': dataset_flat['downloadCount'],
        'modifyingViewUid': dataset.get('modifyingViewUid'),
        'has_viewFilters': 'viewFilters' in dataset,
    }
    return dataset_info

def extract_dataset_table_info():
    dt = DumpTruck(dbname = '/tmp/table_info.db')
    dt.create_table({'portal': 'abc', 'id': 'abcd-efgh'}, 'table_info')
    dt.create_index(['portal', 'id'], 'table_info', unique = True)
    dt.create_index(['tableId'], 'table_info', unique = False)
    done = set([tuple(row.keys()) for row in dt.execute('SELECT portal, id FROM table_info')])
    for portal in os.listdir('data'):
        for viewid in os.listdir(os.path.join('data', portal, 'views')):
            if (portal, viewid) in done:
                continue
            d = _dataset_table_info(portal, viewid)
            if d == None:
                continue
            dt.upsert(d, 'table_info')

def build_table_from_db(dbname = '/tmp/table_info.db'):
    dt = DumpTruck(dbname = dbname)
    tableIds = [row['tableId'] for row in dt.execute('''
SELECT tableId, count(*)
FROM table_info
GROUP BY tableId
ORDER BY count(*) DESC
limit 2;
''')]

    try:
        os.mkdir('geneology')
    except OSError:
        pass
    json.dump(tableIds, open(os.path.join('geneology', 'index.json'), 'w'))

    for tableId in tableIds:
        result = {
            'source': dt.execute('SELECT * FROM table_info WHERE tableId = ? ORDER BY createdAt ASC LIMIT 1', [tableId])[0],
            'datasets': {},
        }
        for dataset in dt.execute('SELECT * FROM table_info WHERE tableId = ?', [tableId]):
            if dataset['id'] not in result['datasets']:
                result['datasets'][dataset['id']] = dataset
                result['datasets'][dataset['id']]['portals'] = []

            result['datasets'][dataset['id']]['portals'].append(dataset['portal'])

        result['datasets'] = result['datasets'].values()
        for dataset in result['datasets']:
            del dataset['portal']
        json.dump(result, open(os.path.join('geneology', '%d.json' % tableId), 'w'))
