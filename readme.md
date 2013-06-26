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

    $ find data -type f -exec grep dataType {} \;|sort|uniq


## Predicting view counts
What sorts of datasets get viewed more?
