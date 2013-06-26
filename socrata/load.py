import os, json
from collections import OrderedDict

def load(data_dir, portal, viewid),:
    '''
    Load a metadata file. Return it as a  array.

    Parameters:

    - `portal`: String portal name (like "explore.data.gov")
    - `viewid`: Socrata 4x4 view id
    '''
    fp = open(os.path.join(data_dir, portal, viewid), 'r')
    original_data = json.load(fp)
    fp.close()

    return OrderedDict([
        ('portal', portal),
        ('viewid', viewid),
    ])

def concat_to_matrix(rows):
    '''
    Return a numpy matrix of the table.

    Parameters:

    - `rows`: An iterable of dicts
    '''
