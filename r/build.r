library(knitr)
if (!('socrata' %in% ls())) {
  socrata <- read.csv('../socrata.csv')
}
knit('summary.Rmd', 'readme.md')
