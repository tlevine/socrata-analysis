import os, json
from collections import OrderedDict, Counter

import numpy as np


DATATYPES = [
    "calendar_date",
    "checkbox",
    "dataset_link",
    "date",
    "document",
    "document_obsolete",
    "drop_down_list",
    "email",
    "flag",
    "geospatial",
    "html",
    "list",
    "location",
    "money",
    "nested_table",
    "number",
    "object",
    "percent",
    "phone",
    "photo",
    "photo_obsolete",
    "stars",
    "text",
    "url",
]

PERSONKEYS = [
    "id",
    "displayName",
    "emailUnsubscribed",
    "privacyControl",
    "profileLastModified",
    "roleName",
    "screenName",
]

def _column_types(columns):
    c = Counter([column["dataTypeName"] for column in columns])
    return [('ncol.' + k,c[k]) for k in sorted(DATATYPES)]

def load(data_dir, portal, viewid):
    '''
    Load a metadata file. Return it as a  array.

    Parameters:

    - `portal`: String portal name (like "explore.data.gov")
    - `viewid`: Socrata 4x4 view id
    '''
    fp = open(os.path.join(data_dir, portal, 'views', viewid), 'r')
    original_string = fp.read()
    fp.close()

    if original_string == '':
        return None
    original_data = json.loads(original_string)

    out = [
        ('portal', portal),
        ('id', original_data['id']),
        ('name', original_data['name']),
        ('attribution', original_data.get('attribution', None)),
        ('averageRating', original_data['averageRating']),
        ('category', original_data.get('category', None)),
        ('createdAt', original_data.get('createdAt', None)),
        ('description', original_data.get('description', None)),
        ('displayType', original_data.get('displayType', None)),
        ('downloadCount', original_data['downloadCount']),
        ('numberOfComments', original_data['numberOfComments']),
        ('oid', original_data['oid']),
        ('publicationAppendEnabled', original_data['publicationAppendEnabled']),
        ('publicationDate', original_data.get('publicationDate', None)),
        ('publicationStage', original_data['publicationStage']),
        ('publicationGroup', original_data.get('publicationGroup', None)),
    #   ('rowClass', original_data['rowClass']),
        ("rowsUpdatedBy", original_data.get('rowsUpdatedBy', None)), # parent dataset
        ("rowsUpdatedAt", original_data.get('rowsUpdatedAt', None)), # parent dataset
        ('signed', original_data['signed']),
        ('tableId', original_data['tableId']),
        ('totalTimesRated', original_data['totalTimesRated']),
        ('viewCount', original_data['viewCount']),
        ('viewLastModified', original_data.get('viewLastModified', None)),
        ('viewType', original_data['viewType']),
    ]

    if len(original_data['columns']) == 0:
        out.append(('nrow', 0))
    elif "cachedContents" in original_data['columns'][0]:
        out.append(('nrow',
            original_data['columns'][0]["cachedContents"]["non_null"] + \
            original_data['columns'][0]["cachedContents"]["null"]))
    else:
        out.append(('nrow', None))
    out.append(('ncol', len(original_data['columns'])))
    out.extend(_column_types(original_data['columns']))

    for person in ['owner', 'tableAuthor']:
        for key in PERSONKEYS:
            out.append(('%s.%s' % (person, key), original_data[person].get(key, None)))
        out.append(('%s.nrights' % person, len(original_data[person].get('rights', []))))

    for countable in sorted(['flags', 'metadata', 'tags', 'displayFormat', 'rights']):
        out.append(('n' + countable, len(original_data.get(countable, []))))

    return OrderedDict(out)

def concat_to_array(rows):
    '''
    Return a numpy matrix of the table.

    Parameters:

    - `rows`: An iterable of OrderedDicts
    '''
    rows = iter(rows)
    try:
        firstrow = rows.next()
    except StopIteration:
        raise ValueError('You must pass at least one row.')

    columns = [np.array([cell]) for cell in firstrow.values()]
    for row in rows:
        for i, v in enumerate(row.values()):
            columns[i] = np.append(columns[i], v)

    return np.array(columns)
