library(ggplot2)
library(reshape2)

date.variables <- c('createdAt','publicationDate', 'rowsUpdatedAt', 'viewLastModified')
if (!('socrata.deduplicated' %in% ls())) {
  socrata.deduplicated <- read.csv('../socrata-deduplicated.csv')

  .columns <- c('portal','id','publicationStage', 'publicationGroup', date.variables)
  s <- socrata.deduplicated[.columns]
  s$createdAt <- as.Date(as.POSIXct(s$createdAt, origin = '1970-01-01'))
  s$publicationDate <- as.Date(as.POSIXct(s$publicationDate, origin = '1970-01-01'))
  s$rowsUpdatedAt <- as.Date(as.POSIXct(s$rowsUpdatedAt, origin = '1970-01-01'))
  s$viewLastModified <- as.Date(as.POSIXct(s$viewLastModified, origin = '1970-01-01'))
  s$date <- s$createdAt
  s[is.na(s$date),'date'] <- s[is.na(s$createdAt),'publicationDate']
  s$publicationStage <- factor(s$publicationStage)
}

s$has.been.updated <- !is.na(s$rowsUpdatedAt) & s$publicationDate < s$rowsUpdatedAt

s.molten <- melt(s[c('portal','id',date.variables)], id.vars = c('portal','id','createdAt','publicationDate'), variable.name = 'update.type', value.name = 'update.date')

p1 <- ggplot(s.molten) +
  aes(x = publicationDate, y = (update.date - publication), group = update.type, color = update.type) +
  facet_wrap(~ portal)
