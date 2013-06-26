Socrata Analysis
======
I [downloaded](https://github.com/tlevine/socrata-download) the metadata files
for all of the Socrata datasets on all of the Socrata portals as of
approximately June 23, 2013. Let's do something fun with them.

## Plumbing

### Downloading data
First, get the data by running the socrata downloader or downloading the June 23 dump.

    wget http://socrata.appgen.me/data.tar.gz
    tar xzf data.tar.gz

This will result in a directory called `data`. Once this directory exists,
you can run the various analyses that are documented below.

### Running tests
Also, you can run the tests like so from the root directory.

    nosetests

### Schema
These are the various possible column dataTypes.

    $ find data -type f -exec grep dataType {} \;|sort|sed 's/^ *//'|uniq
    "dataTypeName" : "calendar_date",
    "dataTypeName" : "checkbox",
    "dataTypeName" : "dataset_link",
    "dataTypeName" : "date",
    "dataTypeName" : "document",
    "dataTypeName" : "document_obsolete",
    "dataTypeName" : "drop_down_list",
    "dataTypeName" : "email",
    "dataTypeName" : "flag",
    "dataTypeName" : "geospatial",
    "dataTypeName" : "html",
    "dataTypeName" : "list",
    "dataTypeName" : "location",
    "dataTypeName" : "money",
    "dataTypeName" : "nested_table",
    "dataTypeName" : "number",
    "dataTypeName" : "object",
    "dataTypeName" : "percent",
    "dataTypeName" : "phone",
    "dataTypeName" : "photo",
    "dataTypeName" : "photo_obsolete",
    "dataTypeName" : "stars",
    "dataTypeName" : "text",
    "dataTypeName" : "url",
    "item" : "There is inconsistency key usage in DataType.dataTypes ArrayCollectionPlus.  The datatype class uses name as key while the datatype manager uses id. This does not address the issue.\n\n\n\nCustomerDataType panel is the only area affected I know about that was affected by this bug.  But it was changed to use DataType.dataTypesByDB in bug#615."


## Predicting view counts
What sorts of datasets get viewed more?
