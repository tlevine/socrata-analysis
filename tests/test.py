import os,json
from collections import Counter, OrderedDict

import nose.tools as n

import socrata

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
def test_column_types():
    'The appropriate column types should be extracted.'
    columns = json.load(open(os.path.join('fixtures','data-input','data.cityofnewyork.us','views','hdr6-7r95')))['columns']
    n.assert_list_equal(OrderedDict(socrata._column_types(columns)).keys(), ['ncol.%s' % dt for dt in DATATYPES])

def test_load():
    IN_DIR = os.path.join('fixtures','data-input')
    OUT_DIR = os.path.join('fixtures','data-output')
    for portal in os.listdir(OUT_DIR):
        for viewid in os.listdir(os.path.join(OUT_DIR,portal,'views')):
            yield check_load_keys, portal, viewid
            yield check_load_values, portal, viewid

def check_load_values(portal,viewid):
    observed = socrata.load(os.path.join('fixtures', 'data-input'),portal,viewid)
    expected = json.load(open(os.path.join('fixtures','data-output',portal,'views',viewid)))
    if expected == None:
        n.assert_is_none(observed)
    else:
        for key in set(observed.keys()).union(expected.keys()):
            n.assert_in(key, observed.keys(), msg = 'I expected the output to include the key "%s", but I did not observe this key.' % key)
            n.assert_in(key, expected.keys(), msg = 'I unexpectedly observed the key "%s".' % key)
            n.assert_equal(observed[key], expected[key], 'For key "%s", I observed "%s" and expected "%s".' % (key, observed[key], expected[key]))

def check_load_keys(portal,viewid):
    'After I load a file, it should have the right keys in the right order.'
    observed = socrata.load(os.path.join('fixtures','data-input'),portal,viewid)
    expected = [
        "portal",
        "id",
        "name",
        "attribution",
        "averageRating",
        "category",
        "createdAt",
        "description",
        "displayType",
        "downloadCount",
        "numberOfComments",
        "oid",
        "publicationAppendEnabled",
        "publicationDate",
        "publicationStage",
        "publicationGroup",
    #   "rowClass",
        "rowsUpdatedBy",
        "rowsUpdatedAt",
        "signed",
        "tableId",
        "totalTimesRated",
        "viewCount",
        "viewLastModified",
        "viewType",
        "nrow",
        "ncol",
        "ncol.calendar_date",
        "ncol.checkbox",
        "ncol.dataset_link",
        "ncol.date",
        "ncol.document",
        "ncol.document_obsolete",
        "ncol.drop_down_list",
        "ncol.email",
        "ncol.flag",
        "ncol.geospatial",
        "ncol.html",
        "ncol.list",
        "ncol.location",
        "ncol.money",
        "ncol.nested_table",
        "ncol.number",
        "ncol.object",
        "ncol.percent",
        "ncol.phone",
        "ncol.photo",
        "ncol.photo_obsolete",
        "ncol.stars",
        "ncol.text",
        "ncol.url",

        "owner.id",
        "owner.displayName",
        "owner.emailUnsubscribed",
        "owner.privacyControl",
        "owner.profileLastModified",
        "owner.roleName",
        "owner.screenName",
        "owner.nrights",

        "tableAuthor.id",
        "tableAuthor.displayName",
        "tableAuthor.emailUnsubscribed",
        "tableAuthor.privacyControl",
        "tableAuthor.profileLastModified",
        "tableAuthor.roleName",
        "tableAuthor.screenName",
        "tableAuthor.nrights",

        "ndisplayFormat",
        "nflags",
        "nmetadata",
        "nrights",
        "ntags",
    ]
    if hasattr(observed, 'keys'):
        n.assert_equal(observed.keys(), expected)
    else:
        n.assert_is_none(observed)
