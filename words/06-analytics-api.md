Some portals expose an analytics page
Let's see what we can get from that.

[This page](https://data.oregon.gov/analytics) makes a bunch
of AJAX requests, including

    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&method=series&slice=DAILY&_=1376438538377
    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&_=1376438538384
    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&method=top&top=DATASETS&_=1376438538392
    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&method=top&top=REFERRERS&_=1376438538397
    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&method=top&top=SEARCHES&_=1376438538402
    https://data.oregon.gov/api/site_metrics.json?start=1375315200000&end=1376438399999&method=top&top=EMBEDS&_=1376438538409
