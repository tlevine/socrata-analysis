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
    n.assert_list_equal(OrderedDict(socrata._column_types(columns)).keys(), DATATYPES)

def test_load():
    'Run all of the fixtures.'
    pass

def test_load_keys():
    'After I load a file, it should have the right keys in the right order.'
    observed = socrata.load(os.path.join('fixtures','data-input'),'data.cityofnewyork.us','hdr6-7r95').keys()
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
        "rowClass",
        "signed",
        "tableId",
        "totalTimesRated",
        "viewCount",
        "viewLastModified",
        "viewType",
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
    ]
    n.assert_equal(observed, expected)
