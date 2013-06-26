import os, json

def load(portal, viewid):
    '''
    Load a metadata file. Return it as a  array.

    Parameters:

    - `portal`: String portal name (like "explore.data.gov")
    - `viewid`: Socrata 4x4 view id
    '''
    fp = open(os.path.join('data', portal, viewid), 'r')
    original_data = json.load(fp)
    fp.close()

    return

def concat_to_matrix(rows):
    '''
    Return a numpy matrix of the table.

    Parameters:

    - `rows`: An iterable of dicts
    '''
