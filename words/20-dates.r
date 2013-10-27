if (!('socrata.deduplicated' %in% ls())) {
  socrata.deduplicated <- read.csv('../socrata-deduplicated.csv')

  s <- socrata.deduplicated[c('portal','id','createdAt','publicationDate','publicationStage', 'publicationGroup', 'rowsUpdatedAt', 'viewLastModified')]
  s$createdAt <- as.Date(as.POSIXct(s$createdAt, origin = '1970-01-01'))
  s$publicationDate <- as.Date(as.POSIXct(s$publicationDate, origin = '1970-01-01'))
  s$rowsUpdatedAt <- as.Date(as.POSIXct(s$rowsUpdatedAt, origin = '1970-01-01'))
  s$viewLastModified <- as.Date(as.POSIXct(s$viewLastModified, origin = '1970-01-01'))
  s$date <- s$createdAt
  s[is.na(s$date),'date'] <- s[is.na(s$createdAt),'publicationDate']
  s$publicationStage <- factor(s$publicationStage)
}
