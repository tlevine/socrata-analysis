library(ggplot2)
library(reshape2)
library(lubridate)
library(scales)

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

s.molten <- melt(s, measure.vars = c('rowsUpdatedAt','viewLastModified'), variable.name = 'update.type', value.name = 'update.date')
s.molten$update.date <- as.Date('1970-01-01') + lubridate::days(s.molten$update.date)
s.molten$days.since.update <- as.numeric(difftime(
  as.Date(Sys.time()), s.molten$update.date, units = 'days'))
s.molten$update.type <- factor(s.molten$update.type,
  levels = c('rowsUpdatedAt', 'viewLastModified'))
levels(s.molten$update.type) <- c('rows','view')

p1 <- ggplot(s.molten) +
  aes(x = publicationDate, y = days.since.update, group = update.type,
    shape = update.type, color = publicationGroup) +
  facet_wrap(~ portal) + geom_point() +
  scale_x_date('Date of dataset publication') +
  scale_y_continuous('Days since the dataset has been updated') +
  scale_color_continuous('Publication group number', labels = comma) +
  ggtitle('How up-to-date are the datasets?')
