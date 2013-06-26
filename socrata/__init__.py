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

def _column_types(columns):
    c = Counter([column["dataTypeName"] for column in columns])
    return [(k,c[k]) for k in sorted(DATATYPES)]

def load(data_dir, portal, viewid):
    '''
    Load a metadata file. Return it as a  array.

    Parameters:

    - `portal`: String portal name (like "explore.data.gov")
    - `viewid`: Socrata 4x4 view id
    '''
    fp = open(os.path.join(data_dir, portal, 'views', viewid), 'r')
    original_data = json.load(fp)
    fp.close()

    out = [
        ('portal', portal),
        ('id', original_data['id']),
        ('name', original_data['name']),
        ('attribution', original_data['attribution']),
        ('averageRating', original_data['averageRating']),
        ('category', original_data['category']),
        ('createdAt', original_data['createdAt']),
        ('description', original_data['description']),
        ('displayType', original_data['displayType']),
        ('downloadCount', original_data['downloadCount']),
        ('numberOfComments', original_data['numberOfComments']),
        ('oid', original_data['oid']),
        ('publicationAppendEnabled', original_data['publicationAppendEnabled']),
        ('publicationDate', original_data['publicationDate']),
        ('publicationStage', original_data['publicationStage']),
        ('rowClass', original_data['rowClass']),
        ('signed', original_data['signed']),
        ('tableId', original_data['tableId']),
        ('totalTimesRated', original_data['totalTimesRated']),
        ('viewCount', original_data['viewCount']),
        ('viewLastModified', original_data['viewLastModified']),
        ('viewType', original_data['viewType']),
    ]

    for datatype in DATATYPES:
        key = 'ncol.' + datatype
        value = original_data.get(datatype, 0)
        out.append((key, value))

    return OrderedDict(out)

def concat_to_matrix(rows):
    '''
    Return a numpy matrix of the table.

    Parameters:

    - `rows`: An iterable of dicts
    '''
