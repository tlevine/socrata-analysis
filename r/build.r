library(knitr)
if (!('socrata' %in% ls())) {
  socrata <- read.csv('../socrata.csv', stringsAsFactors = F)
  socrata$createdAt <- as.Date(as.POSIXct(socrata$createdAt, origin = '1970-01-01'))
}
knit('summary.Rmd', 'readme.md')
