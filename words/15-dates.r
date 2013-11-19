library(ggplot2)
library(reshape2)
library(lubridate)
library(scales)
library(plyr)
library(sqldf)
library(directlabels)
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
    socrata.deduplicated$rowsUpdatedAt - socrata.deduplicated$publicationDate > 3600)

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
}

# ny <- subset(s.molten, has.been.updated & portal == 'data.cityofnewyork.us' & update.date == '2013-06-28')

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

p3 <- ggplot(subset(s.window, update.type == 'rows')) +
  aes(x = weeks, y = prop, size = count) + geom_line(alpha = 0.5) +
  ylab('Proportion datasets older than the cutoff that have been updated since the cutoff') +
  scale_size_continuous('Number of datasets in the portal') +
  ggtitle('How many old datasets have been updated recently, by portal?') +
  xlab('Cutoff (number of weeks before today)') + facet_wrap(~ portal)

print('Add a plot `p4` explaining why it is not interesting that the line moves when the portal has few datasets.')

p5 <- ggplot(socrata.deduplicated) +
  aes(x = portal, group = has.been.updated.factor, fill = has.been.updated.factor) +
  geom_bar() + coord_flip() +
  ylab('') + xlab('Number of datasets on the portal') +
  scale_fill_discrete('Has the dataset ever been updated?') +
  ggtitle('Hardly any datasets get updated.')

p6 <- ggplot(subset(s.molten, has.been.updated & update.type == 'rows')) +
  aes(x = update.date) + geom_histogram(binwidth = 30) +
  facet_wrap(~ portal)

p7 <- ggplot(subset(s.molten, has.been.updated & update.type == 'rows' & (portal == 'data.cityofnewyork.us' | portal == 'cookcounty.socrata.com' | portal == 'data.cityofchicago.org' | portal == 'data.hawaii.gov' | portal == 'data.kingcounty.gov' | portal == 'data.maryland.gov' | portal == 'data.medicare.gov' | portal == 'data.mo.gov' | portal == 'data.ny.gov' | portal == 'data.oregon.gov' | portal == 'data.sunlightlabs.com' | portal == 'opendata.go.ke'))) +
  aes(x = update.date) + geom_histogram(binwidth = 30) +
  facet_wrap(~ portal) +
  scale_x_date('Month') +
  ylab('Number of datasets updated that month')

p8 <- ggplot(subset(s.molten, has.been.updated & (portal == 'data.cityofnewyork.us' | portal == 'opendata.go.ke' | portal == 'data.oregon.gov'))) +
  aes(x = update.date) + geom_histogram(binwidth = 1) +
  scale_x_date('Day', breaks = pretty_breaks(12), labels = date_format('%B %Y')) +
  facet_wrap(~ portal, nrow = 3, ncol = 1) +
  ylab('Number of datasets updated today')

p9 <- ggplot(subset(s.molten, has.been.updated & update.type == 'rows' & (portal == 'opendata.go.ke' | portal == 'data.oregon.gov' | portal == 'data.cityofnewyork.us'))) +
  aes(y = publicationDate, x = update.date, label = id) +
  scale_y_date('Publication date', breaks = pretty_breaks(12), labels = date_format('%B %Y')) +
  scale_x_date('Update date', breaks = pretty_breaks(12), labels = date_format('%B %Y')) +
  facet_wrap(~ portal, nrow = 3, ncol = 1) + geom_point(alpha = 0.3)

p10 <- ggplot(subset(s.molten, has.been.updated & update.type == 'rows' & (portal == 'data.oregon.gov' | portal == 'data.cityofnewyork.us'))) +
  aes(y = publicationDate, x = update.date, label = id) +
  scale_y_date('Publication date', breaks = pretty_breaks(12), labels = date_format('%B %Y')) +
  scale_x_date('Update date', breaks = pretty_breaks(12), labels = date_format('%B %Y')) +
  facet_wrap(~ portal, nrow = 2, ncol = 1) + geom_point(alpha = 0.3) +
  geom_text() + xlim(as.Date(c(paste0('2013-',c('03','08'), '-01'))))

p11 <- ggplot(subset(s.molten, has.been.updated & update.type == 'rows' & (portal == 'opendata.go.ke' | portal == 'data.oregon.gov' | portal == 'data.cityofnewyork.us'))) +
  aes(x = publicationDate, y = update.minus.publish, label = id) +
  scale_x_date('Initial publication date', breaks = pretty_breaks(12), labels = date_format('%B %Y')) +
  facet_wrap(~ portal, nrow = 3, ncol = 1) + geom_point(alpha = 0.3)

p12 <- ggplot(updates.2013) +
  aes(x = portal) + geom_histogram() +
  ggtitle('These are all of the Socrata datasets published before 2013 that have been updated since.')

p13 <- ggplot(updates.2013) +
  aes(x = portal, label = id, y = 1) + geom_text(position = 'stack') +
  scale_y_continuous('', breaks = c()) +
  ggtitle('These are all of the Socrata datasets published before 2013 that have been updated since.')

p14 <- ggplot(updates.ever) +
  aes(x = as.numeric(portal) + 0.2 * has.been.updated, y = familyDownloadCount, color = has.been.updated.factor) +
  scale_x_continuous('', breaks = 1:length(levels(updates.ever$portal)), labels = levels(updates.ever$portal)) +
  scale_y_log10('How many times data has been downloaded', labels = comma) +
  scale_color_discrete('Has the dataset ever been updated?') +
  geom_point(alpha = 0.5) + coord_flip() +
  ggtitle('Datasets that get downloaded more tend also to be more up-to-date.\n(Each point is a family/table of datasets on a Socrata data portal.)')

m14.wilcox <- wilcox.test(socrata.deduplicated$familyDownloadCount[socrata.deduplicated$has.been.updated],
                          socrata.deduplicated$familyDownloadCount[!socrata.deduplicated$has.been.updated])
m14.medians <- c(median(socrata.deduplicated$familyDownloadCount[socrata.deduplicated$has.been.updated]),
                 median(socrata.deduplicated$familyDownloadCount[!socrata.deduplicated$has.been.updated]))
m14.student <- t.test(socrata.deduplicated$familyDownloadCount[socrata.deduplicated$has.been.updated],
                      socrata.deduplicated$familyDownloadCount[!socrata.deduplicated$has.been.updated])
m14.means <- c(mean(socrata.deduplicated$familyDownloadCount[socrata.deduplicated$has.been.updated]),
               mean(socrata.deduplicated$familyDownloadCount[!socrata.deduplicated$has.been.updated]))

p15 <- p14 + aes(size = familyNrow) +
  scale_size_continuous('Number of records in the dataset', labels = comma)

p16 <- ggplot(updates.2013.joined) +
  aes(color = portal, label = paste0('https://',portal,'\n/d/',id), x = familyNrow, y = familyDownloadCount) +
  scale_y_log10('Number of downloads', breaks = 10^(1:5), labels = comma) +
  scale_x_log10('Number of records in the dataset', breaks = 10^(1:5), labels = comma) +
  ggtitle('These are all of the Socrata datasets published before 2013 that have been updated since.') +
  geom_text()

p17 <- ggplot(subset(s.molten, update.type == 'rows')) +
  aes(x = publicationDate, y = portal, color = has.been.updated.factor) +
  geom_point(position = 'jitter') +
  scale_x_date('Date of table publication') + ylab('') +
  scale_color_discrete('Has the dataset ever been updated?') +
  ggtitle('Dataset publication and updating')

p18 <- ggplot(monthly.dataset.count) +
  aes(x = month, y = dataset.count, color = portal, label = portal) +
  geom_line() + xlim(c(min(months$month), max(months$month) + 100))
p18 <- direct.label(p18, list(last.points))
