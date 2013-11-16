library(ggplot2)
library(reshape2)
library(lubridate)
library(scales)
library(plyr)
library(sqldf)
TODAY <- as.Date(Sys.time())

date.variables <- c('createdAt','publicationDate', 'rowsUpdatedAt', 'viewLastModified')
.columns <- c('portal','id','publicationStage', 'publicationGroup', date.variables)
if (!('socrata.deduplicated' %in% ls())) {
  print(2)
  socrata.deduplicated.orig <- read.csv('../socrata-deduplicated.csv')
  socrata.deduplicated <- subset(socrata.deduplicated.orig, portal != 'opendata.socrata.com')
  socrata.deduplicated <- sqldf('SELECT * FROM [socrata.deduplicated] GROUP BY "tableId"')

  socrata.deduplicated$has.been.updated <- (
    (!is.na(socrata.deduplicated$rowsUpdatedAt)) &
    socrata.deduplicated$rowsUpdatedAt - socrata.deduplicated$publicationDate > 3600)

  print(3)
  s <- socrata.deduplicated[.columns]
  s$createdAt <- as.Date(as.POSIXct(s$createdAt, origin = '1970-01-01'))
  s$publicationDate <- as.Date(as.POSIXct(s$publicationDate, origin = '1970-01-01'))
  s$rowsUpdatedAt <- as.Date(as.POSIXct(s$rowsUpdatedAt, origin = '1970-01-01'))
  s$viewLastModified <- as.Date(as.POSIXct(s$viewLastModified, origin = '1970-01-01'))
  s$date <- s$createdAt
  s[is.na(s$date),'date'] <- s[is.na(s$createdAt),'publicationDate']
  s$publicationStage <- factor(s$publicationStage)

  s$has.been.updated <- !is.na(s$rowsUpdatedAt) & s$publicationDate < s$rowsUpdatedAt

  print(4)
  s.molten <- melt(s, measure.vars = c('rowsUpdatedAt','viewLastModified'), variable.name = 'update.type', value.name = 'update.date')
  s.molten$update.date <- as.Date('1970-01-01') + lubridate::days(s.molten$update.date)
  s.molten$days.since.update <- as.numeric(difftime(
    TODAY, s.molten$update.date, units = 'days'))
  s.molten$update.type <- factor(s.molten$update.type,
    levels = c('rowsUpdatedAt', 'viewLastModified'))
  levels(s.molten$update.type) <- c('rows','view')

  s.molten$one.year <- difftime(s.molten$update.date, s.molten$publicationDate, units = 'weeks') > 52

  print(5)
  s.daily <- ddply(s.molten, c('portal', 'update.date'), function(df) {
    df.subset <- subset(df, difftime(TODAY, df$publicationDate, units = 'weeks') > 52)
    c(prop.up.to.date = mean(df.subset$one.year))
  })
  s.daily$prop.up.to.date <- factor(s.daily$prop.up.to.date,
    levels = names(sort(s.daily$prop.up.to.date)))

  print(6)
  s.window <- ddply(data.frame(weeks = (2 * 52):0), 'weeks', function(nweeks.df) {
    nweeks <- nweeks.df$weeks[1]

    ddply(s.molten, c('portal','update.type'), function(df.full) {
      df <- subset(df.full, difftime(TODAY, df.full$publicationDate, units = 'weeks') > nweeks)
      df$up.to.date <- difftime(TODAY, df$update.date, units = 'weeks') < nweeks
      df$up.to.date[is.na(df$up.to.date)] <- FALSE
      c(prop = sum(df$up.to.date) / nrow(df), count = nrow(df))
    })
  })
  print(7)
}

p1 <- ggplot(subset(s.molten, update.type == 'rows')) +
  aes(x = publicationDate, y = days.since.update, color = publicationGroup) +
  facet_wrap(~ portal) + geom_point() +
  scale_x_date('Date of table publication') +
  scale_y_continuous('Days since the table has been updated') +
  scale_color_continuous('Publication group number', labels = comma) +
  ggtitle('How up-to-date are the data?')


p2 <- ggplot(s.molten) +
  aes(x = publicationDate, color = one.year,
    group = interaction(one.year, update.type),
    linetype = update.type) +
  geom_line(stat='bin')

p4 <- ggplot(subset(s.window, update.type == 'rows')) +
  aes(x = weeks, y = prop, size = count) + geom_line(alpha = 0.5) +
  ylab('Proportion datasets older than the cutoff that have been updated since the cutoff') +
  scale_size_continuous('Number of datasets in the portal') +
  ggtitle('How many old datasets have been updated recently, by portal?') +
  xlab('Cutoff (number of weeks before today)') + facet_wrap(~ portal)


socrata.deduplicated$portal <- factor(socrata.deduplicated$portal, levels = names(sort(table(socrata.deduplicated$portal))))
socrata.deduplicated$has.been.updated.factor <- factor(socrata.deduplicated$has.been.updated,levels = c(TRUE, FALSE))
levels(socrata.deduplicated$has.been.updated.factor) <- c('Yes','No')

p5 <- ggplot(socrata.deduplicated) +
  aes(x = portal, group = has.been.updated.factor, fill = has.been.updated.factor) +
  geom_bar() + coord_flip() +
  ylab('') + xlab('Number of datasets on the portal') +
  scale_color_discrete('Has the dataset ever been updated?') +
  ggtitle('Hardly any datasets get updated.')

p6 <- ggplot(subset(s.molten, update.type == 'rows')) +
  aes(x = update.date) + geom_histogram(binwidth = 30) +
  facet_wrap(~ portal)

updates.by.portal <- ddply(s.molten, 'portal', function(df) {
  c(
    portal = df[1,'portal'],
    datasets.updated = nrow(df)
  )
})

p7 <- ggplot() +
  aes(x = ) + geom_histogram(binwidth = 30) +
  facet_wrap(~ portal)

p8 <- ggplot(subset(s.molten, update.type == 'rows' & (portal == 'data.cityofnewyork.us' | portal == 'cookcounty.socrata.com' | portal == 'data.cityofchicago.org' | portal == 'data.hawaii.gov' | portal == 'data.kingcounty.gov' | portal == 'data.maryland.gov' | portal == 'data.medicare.gov' | portal == 'data.mo.gov' | portal == 'data.ny.gov' | portal == 'data.oregon.gov' | portal == 'data.sunlightlabs.com' | portal == 'opendata.go.ke'))) +
  aes(x = update.date) + geom_histogram(binwidth = 30) +
  facet_wrap(~ portal) +
  scale_x_date('Month') +
  ylab('Number of datasets updated that month')
