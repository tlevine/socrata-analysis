def test_load():
    'Run all of the fixtures.'
    pass

def test_load_keys():
    'After I load a file, it should have the right keys in the right order.'
    observed = load().keys()
    expected = [
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

## Predicting view counts
What sorts of datasets get viewed more?
