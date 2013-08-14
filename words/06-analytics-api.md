Some portals expose an analytics page
Let's see what we can get from that.

## AJAX requests on the analytics page
[This page](https://data.oregon.gov/analytics) makes a bunch
of AJAX requests, including

    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&method=series&slice=DAILY&_=1376438538377
    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&_=1376438538384
    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&method=top&top=DATASETS&_=1376438538392
    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&method=top&top=REFERRERS&_=1376438538397
    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&method=top&top=SEARCHES&_=1376438538402
    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&method=top&top=EMBEDS&_=1376438538409

There's also a mechanism for batch requests. Some of the above methods
return 4x4 ids, and the page seems to use the batch endpoint to get the
metadata for multiple datasets in one request.

    https://data.oregon.gov/api/batches

The `site_metrics.json` endpoint is the interesting one,
so I figured out how it works. 

## Site metrics endpoint

    GET /api/site_metrics.json

You access this endpoint by making a typical GET request; you don't need
any special cookie, header, or API key. Two query arguments are required

* `start`
* `end`

These are both dates, represented as milliseconds since January 1, 1970.
(Something like <script>document.write((new Date()).getTime())</script><noscript>1376439688459</noscript>)
These arguments define the range within which the analytics will be aggregated.

This endpoint exposes three methods.

* `top`
* `series`
* no method.

### Most popular (`top`)

### Site-wide statistics

### Site-wide statistics by time interval

