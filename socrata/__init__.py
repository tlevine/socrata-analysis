import os, json
from collections import OrderedDict, Counter

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
        ('category', original_data['category']),
        ('createdAt', original_data['createdAt']),
        ('description', original_data.get('description', None)),
        ('displayType', original_data.get('displayType', None)),
        ('downloadCount', original_data['downloadCount']),
        ('numberOfComments', original_data['numberOfComments']),
        ('oid', original_data['oid']),
        ('publicationAppendEnabled', original_data['publicationAppendEnabled']),
        ('publicationDate', original_data['publicationDate']),
        ('publicationStage', original_data['publicationStage']),
    #   ('rowClass', original_data['rowClass']),
        ('signed', original_data['signed']),
        ('tableId', original_data['tableId']),
        ('totalTimesRated', original_data['totalTimesRated']),
        ('viewCount', original_data['viewCount']),
        ('viewLastModified', original_data['viewLastModified']),
        ('viewType', original_data['viewType']),
    ]

    out.append(('nrow', original_data['columns'][0]["cachedContents"]["non_null"] + original_data['columns'][0]["cachedContents"]["null"]))
    out.append(('ncol', len(original_data['columns'])))
    out.extend(_column_types(original_data['columns']))

    for person in ['owner', 'tableAuthor']:
        for key in PERSONKEYS:
            out.append(('%s.%s' % (person, key), original_data[person].get(key, None)))
        out.append(('%s.nrights' % person, len(original_data[person].get('rights', []))))

    out.append(('nflags', len(original_data.get('flags', []))))
    out.append(('ntags', len(original_data.get('tags', []))))

    return OrderedDict(out)

def concat_to_matrix(rows):
    '''
    Return a numpy matrix of the table.

    Parameters:

    - `rows`: An iterable of dicts
    '''
