import os, json
from collections import OrderedDict

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

    return OrderedDict([
        ('portal', portal),
        ('viewid', viewid),
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
    ])

def concat_to_matrix(rows):
    '''
    Return a numpy matrix of the table.

    Parameters:

    - `rows`: An iterable of dicts
    '''
