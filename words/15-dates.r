library(ggplot2)
library(reshape2)
library(lubridate)
library(scales)
library(plyr)
library(sqldf)
library(directlabels)
library(gridExtra)
TODAY <- as.Date('2013-07-08') # Really a few days before, but just to be safe

date.variables <- c('createdAt','publicationDate', 'rowsUpdatedAt', 'viewLastModified')
.columns <- c('portal','id','publicationStage', 'publicationGroup', date.variables,'has.been.updated', 'has.been.updated.factor')
if (!('socrata.deduplicated' %in% ls())) {
  print(2)
# socrata.deduplicated.orig <- read.csv('../socrata-deduplicated.csv')
  socrata.deduplicated <- subset(socrata.deduplicated.orig, portal != 'opendata.socrata.com')
  socrata.deduplicated <- sqldf('SELECT *, max(nrow) AS familyNrow, sum(downloadCount) AS familyDownloadCount FROM [socrata.deduplicated] GROUP BY "tableId"')

  socrata.deduplicated$has.been.updated <- (
    (!is.na(socrata.deduplicated$rowsUpdatedAt)) &
    socrata.deduplicated$rowsUpdatedAt - socrata.deduplicated$publicationDate > 24 * 3600)

  socrata.deduplicated$portal <- factor(socrata.deduplicated$portal, levels = names(sort(table(socrata.deduplicated$portal))))
  socrata.deduplicated$has.been.updated.factor <- factor(socrata.deduplicated$has.been.updated,levels = c(TRUE, FALSE))
  levels(socrata.deduplicated$has.been.updated.factor) <- c('Yes','No')

  print(3)
  s <- socrata.deduplicated[.columns]
  s$createdAt <- as.Date(as.POSIXct(s$createdAt, origin = '1970-01-01'))
  s$publicationDate <- as.Date(as.POSIXct(s$publicationDate, origin = '1970-01-01'))
  s$rowsUpdatedAt <- as.Date(as.POSIXct(s$rowsUpdatedAt, origin = '1970-01-01'))
  s$viewLastModified <- as.Date(as.POSIXct(s$viewLastModified, origin = '1970-01-01'))
  s$date <- s$createdAt
  s[is.na(s$date),'date'] <- s[is.na(s$createdAt),'publicationDate']
  s$publicationStage <- factor(s$publicationStage)

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
  s.molten$update.minus.publish <- as.numeric(difftime(s.molten$update.date, s.molten$publicationDate, units = 'days'))

  updates.2013 <- subset(s.molten, has.been.updated & update.type == 'rows' & publicationDate < as.Date('2013-01-01') & update.date > as.Date('2013-01-01'))

  updates.2013$url <- paste0('https://',updates.2013$portal,'/d/',updates.2013$id)
  updates.2013.joined <- plyr::join(updates.2013, socrata.deduplicated, type = 'left', by = c('portal','id'))
  updates.2013.joined[c('url','name','familyDownloadCount', 'familyNrow')]

  updates.ever <- plyr::join(subset(s.molten, has.been.updated & update.type == 'rows')[c('portal','id', 'has.been.updated')], socrata.deduplicated, type = 'right', by = c('portal','id'))
  updates.ever$has.been.updated[is.na(updates.ever$has.been.updated)] <- FALSE
  updates.ever$portal <- droplevels(updates.ever$portal)

  print(8)
  months <- data.frame(month = seq.Date(as.Date('2011-01-01'), as.Date('2013-07-01'), by = 'month'))
  months$month.epoch <- as.numeric(strftime(months$month, '%s'))
  monthly.dataset.count <- ddply(months, 'month', function(df) {
    month.epoch <- df[1,'month.epoch']
    sqldf(paste0('SELECT "portal", count(*) "dataset.count" FROM [socrata.deduplicated] WHERE "publicationDate" < \'', month.epoch, '\' GROUP BY "portal"'))
  })
  monthly.dataset.count$dataset.count <- as.numeric(monthly.dataset.count$dataset.count)

  print(9)
  data.cms.gov.raw <- subset(socrata.deduplicated, portal == 'data.cms.gov')[c('id','tableId','publicationDate','rowsUpdatedAt')]
  data.cms.gov.raw$rowsUpdatedAt[data.cms.gov.raw$rowsUpdatedAt - 24 * 3600 < data.cms.gov.raw$publicationDate] <- NA
  data.cms.gov.molten <- melt(data.cms.gov.raw, id.vars = c('id','tableId'), variable.name = 'date.type', value.name = 'date')
  data.cms.gov.molten$date <- as.POSIXct(data.cms.gov.molten$date, origin = '1970-01-01')
  data.cms.gov.molten$date.type <- factor(data.cms.gov.molten$date.type, levels = c('publicationDate','rowsUpdatedAt'))
  levels(data.cms.gov.molten$date.type) <- c('First published','Last updated')
  data.cms.gov.molten$url <- paste0('https://data.cms.gov/d/',data.cms.gov.molten$id)
  data.cms.gov.molten$label <- data.cms.gov.molten$url
  data.cms.gov.molten$label[data.cms.gov.molten$date.type == 'Last updated'] <- ''
  data.cms.gov.molten$hjust <- 1.1
  data.cms.gov.molten$vjust <- 0.35
  data.cms.gov.molten$hjust[data.cms.gov.molten$id == '8j8s-q5gd'] <- 0
  data.cms.gov.molten$vjust[data.cms.gov.molten$id == '8j8s-q5gd'] <- -1.5
}

# ny <- subset(s.molten, has.been.updated & portal == 'data.cityofnewyork.us' & update.date == '2013-06-28')

p1 <- ggplot(subset(s.molten, update.type == 'rows')) +
  aes(x = publicationDate, y = days.since.update) +
  facet_wrap(~ portal) + geom_point() +
  scale_x_date('Date of table publication') +
  scale_y_continuous('Days since the table has been updated') +
# scale_color_continuous('Publication group number', labels = comma) +
  ggtitle('How up-to-date are the data?')


p2 <- ggplot(s.molten) +
  aes(x = publicationDate, color = one.year,
    group = interaction(one.year, update.type),
    linetype = update.type) +
  geom_line(stat='bin')

p3 <- ggplot(subset(s.window, update.type == 'rows')) +
  aes(x = weeks, y = prop, size = count) + geom_line(alpha = 0.5) +
  ylab('Proportion datasets older than the cutoff that have been updated since the cutoff') +
  scale_size_continuous('Number of datasets\nin the portal') +
  ggtitle('How many old datasets have been updated recently, by portal?') +
  theme(legend.position = 'bottom') +
  xlab('Cutoff (number of weeks before today)') + facet_wrap(~ portal)

data.cms.gov.cutoff <- subset(s.window, update.type == 'rows' & portal == 'data.cms.gov')
data.cms.gov.cutoff$date <- TODAY - (7 * as.difftime('24:0:0') * data.cms.gov.cutoff$weeks)

p4.breaks <- seq.Date(as.Date('2011-05-01'), as.Date('2013-07-01'), '2 months')
p4.a <- ggplot(data.cms.gov.cutoff) +
  aes(x = date, y = prop, size = count) + geom_line(alpha = 0.5) +
  aes(xmin = as.Date('2011-04-01'), xmax = as.Date('2013-08-01')) +
  ylab('Proportion of datasets older than the cutoff\nthat have been updated since') +
  scale_size_continuous('Number of datasets\nin data.cms.gov') +
  ggtitle('How many old data.cms.gov datasets have been updated recently?') +
  theme(legend.position = c(0.9,0.5)) +
  scale_x_date('Cutoff date', labels = date_format('%b %Y'), breaks = p4.breaks, minor_breaks = waiver())

p4.b <- ggplot(data.cms.gov.molten) +
  aes(y = factor(tableId), x = date, group = tableId, label = label) +
  aes(xmin = as.POSIXct('2011-04-01'), xmax = as.POSIXct('2013-08-01')) +
  geom_line() + geom_point(aes(color = date.type), size = 6) +
  geom_text(aes(hjust = hjust, vjust = vjust), size = 4) +
  scale_y_discrete('Data table', breaks = c()) +
  scale_color_discrete('Dates') +
  theme(legend.position = c(0.9,0.5)) +
  scale_x_datetime('Date of upload or publication to data.cms.gov', labels = date_format('%b %Y'), breaks = as.POSIXct(p4.breaks), minor_breaks = waiver())

gp4.a <- ggplot_gtable(ggplot_build(p4.a))
gp4.b <- ggplot_gtable(ggplot_build(p4.b))
maxWidth = unit.pmax(gp4.a$widths[2:3], gp4.b$widths[2:3])
gp4.a$widths[2:3] <- maxWidth
gp4.b$widths[2:3] <- maxWidth

p4 <- function() { grid.arrange(gp4.a,gp4.b, heights = c(1/3, 2/3))}

p5 <- ggplot(socrata.deduplicated) +
  aes(x = portal, group = has.been.updated.factor, fill = has.been.updated.factor) +
  geom_bar() + coord_flip() +
  ylab('') + xlab('Number of datasets on the portal') +
  scale_fill_discrete('Has the dataset ever been updated?') +
  theme(legend.position = 'bottom') +
  ggtitle('Hardly any datasets get updated.')

p6 <- ggplot(subset(s.molten, has.been.updated & update.type == 'rows')) +
  aes(x = update.date) + geom_histogram(binwidth = 30) +
  scale_x_date('Month of update', labels = date_format('%b %Y')) +
  ylab('Number of datasets') +
  facet_wrap(~ portal)

p9 <- ggplot(subset(s.molten, has.been.updated & update.type == 'rows')) +
  aes(y = publicationDate, x = update.date, label = id) +
  scale_y_date('Publication date', breaks = pretty_breaks(12), labels = date_format('%B %Y')) +
  scale_x_date('Update date', breaks = pretty_breaks(12), labels = date_format('%B %Y')) +
  geom_point(alpha = 0.4, color = 'red') +
  geom_abline(intercept = 0, slope = 1, color = 'grey') +
  coord_fixed() +
  ggtitle('Publication and update dates of all public datasets hosted on Socrata')

p10 <- p9 +
  annotate('text', x = as.Date('2013-03-15'), y = as.Date('2013-07-01'), label = 'Published recently,\nupdated recently') +
  annotate('text', x = as.Date('2012-02-01'), y = as.Date('2011-06-01'), label = 'Published a long time ago,\nupdated a long time ago') +
  annotate('text', x = as.Date('2013-02-01'), y = as.Date('2011-12-01'), label = 'Published a long time ago,\nupdated recently')

.date.2013 <- as.Date('2013-01-01')
p11 <- p9 +
  annotate('text', x = as.Date('2013-04-01'), y = as.Date('2012-05-01'), label = 'Published before 2013 and\nupdated during 2013') +
  annotate('rect', xmin = .date.2013, ymax = .date.2013, xmax = TODAY, ymin = as.Date('2011-04-01'), alpha = 0.2)

p12 <- ggplot(updates.2013) +
  aes(x = portal) + geom_histogram() +
  ggtitle('These are all of the Socrata datasets published before 2013 that have been updated since.')

p13 <- ggplot(updates.2013) +
  aes(x = portal, label = paste0(portal,'/d/\n',id), y = 1) + geom_text(position = 'stack', size = 4) +
  scale_y_continuous('', breaks = c()) +
  ggtitle('These are all of the Socrata datasets published before 2013 that have been updated since.')

p14 <- ggplot(updates.ever) +
  aes(x = as.numeric(portal) + 0.2 * has.been.updated, y = familyDownloadCount, color = has.been.updated.factor) +
  scale_x_continuous('', breaks = 1:length(levels(updates.ever$portal)), labels = levels(updates.ever$portal)) +
  scale_y_log10('How many times data has been downloaded', labels = comma) +
  scale_color_discrete('Has the dataset ever been updated?') +
  theme(legend.position = 'bottom') +
  geom_point(alpha = 0.5) + coord_flip() +
  ggtitle('Datasets that get downloaded more sort of tend to be more up-to-date.\n(Each point is a family/table of datasets on a Socrata data portal.)')

m14.wilcox <- wilcox.test(socrata.deduplicated$familyDownloadCount[socrata.deduplicated$has.been.updated],
                          socrata.deduplicated$familyDownloadCount[!socrata.deduplicated$has.been.updated])
m14.medians <- c(median(socrata.deduplicated$familyDownloadCount[socrata.deduplicated$has.been.updated]),
                 median(socrata.deduplicated$familyDownloadCount[!socrata.deduplicated$has.been.updated]))
m14.student <- t.test(socrata.deduplicated$familyDownloadCount[socrata.deduplicated$has.been.updated],
                      socrata.deduplicated$familyDownloadCount[!socrata.deduplicated$has.been.updated])
m14.means <- c(mean(socrata.deduplicated$familyDownloadCount[socrata.deduplicated$has.been.updated]),
               mean(socrata.deduplicated$familyDownloadCount[!socrata.deduplicated$has.been.updated]))

p15 <- p14 + aes(y = familyNrow) +
  scale_size_continuous('Number of records in the dataset', labels = comma) +
  scale_y_log10('How many records the dataset has', labels = comma) +
  ggtitle('Datasets that get downloaded more sort of tend to have more records.\n(Each point is a family/table of datasets on a Socrata data portal.)')

m15.wilcox <- wilcox.test(socrata.deduplicated$familyNrow[socrata.deduplicated$has.been.updated],
                          socrata.deduplicated$familyNrow[!socrata.deduplicated$has.been.updated])
m15.medians <- c(median(socrata.deduplicated$familyNrow[socrata.deduplicated$has.been.updated],na.rm=TRUE),
                 median(socrata.deduplicated$familyNrow[!socrata.deduplicated$has.been.updated],na.rm=TRUE))
m15.student <- t.test(socrata.deduplicated$familyNrow[socrata.deduplicated$has.been.updated],
                      socrata.deduplicated$familyNrow[!socrata.deduplicated$has.been.updated])
m15.means <- c(mean(socrata.deduplicated$familyNrow[socrata.deduplicated$has.been.updated],na.rm=TRUE),
               mean(socrata.deduplicated$familyNrow[!socrata.deduplicated$has.been.updated],na.rm=TRUE))

p16 <- ggplot(updates.2013.joined) +
  aes(color = portal, label = paste0('https://',portal,'\n/d/',id), x = familyNrow, y = familyDownloadCount) +
  scale_y_log10('Number of downloads', breaks = 10^(1:5), labels = comma) +
  scale_x_log10('Number of records in the dataset', breaks = 10^(1:5), labels = comma) +
  ggtitle('These are all of the Socrata datasets published before 2013 that have been updated since.') +
  theme(legend.position = 'bottom') +
  geom_text()

p17 <- ggplot(subset(s.molten, update.type == 'rows')) +
  aes(x = publicationDate, y = portal, color = has.been.updated.factor) +
  geom_point(position = 'jitter') +
  scale_x_date('Date of table publication') + ylab('') +
  scale_color_discrete('Has the dataset ever been updated?') +
  theme(legend.position = 'bottom') +
  ggtitle('Dataset publication and updating')

p18 <- ggplot(monthly.dataset.count) +
  aes(x = month, y = dataset.count, color = portal, label = portal) +
  geom_line() + xlim(c(min(months$month), max(months$month) + 100)) +
  xlab('Date') +
  ylab('Number of datasets in the portal') +
  ggtitle('How many datasets are in the different portals?')

p18 <- direct.label(p18, list(last.points))

cat('Explain these two bad alternatives to updating:
1. Replace an old dataset with a new one, changing the 4x4 identifier.
2. Add a new dataset for the new year (maybe with the new year in the title), creating multiple 4x4 identifiers.

Also mention how it would be awesome to be able to set how often a
dataset should be updated and then to be made aware when datasets
are out-of-date. Show how this works in treasury.io.
')
