library(ggplot2)
library(plyr)
library(knitr)
library(scales)
library(reshape2)
library(grDevices)
library(sqldf)

if (!('socrata' %in% ls())) {
  socrata <- read.csv('../socrata.csv', stringsAsFactors = F)
  socrata$createdAt <- as.Date(as.POSIXct(socrata$createdAt, origin = '1970-01-01'))
  socrata$publicationDate <- as.Date(as.POSIXct(socrata$publicationDate, origin = '1970-01-01'))
  socrata$date <- socrata$createdAt
  socrata[is.na(socrata$date),'date'] <- socrata[is.na(socrata$createdAt),'publicationDate']

  socrata.distinct <- sqldf('select * from socrata group by id')
}

if (!('users' %in% ls())) {
  users <- read.csv('../users.csv', stringsAsFactors = F)
  users$profileLastModified <- as.Date(as.POSIXct(users$profileLastModified, origin = '1970-01-01'))
  for (variable in names(users)) {
    users[nchar(users[,variable]) == 0,variable] <- NA
  }
  rownames(users) <- users$id
  users$has.flag <- !is.na(users$flags)
  users$has.role <- !is.na(users$roleName)
}

if (!('user.views' %in% ls())) {
  user.views <- sqldf('
  SELECT
    users.id AS userid,
    socrata.id as viewid,
    nrow, ncol,
    viewType,
    createdAt,
    publicationDate,
    has_flag
  FROM socrata
  LEFT JOIN users
  ON socrata.owner_id = users.id
  GROUP BY socrata.id')
  user.views$date <- user.views$createdAt
  user.views[is.na(user.views$date),'date'] <- user.views[is.na(user.views$createdAt),'publicationDate']
}

# Helpers
listify <- function(datasets) {
  cat(paste(
    paste(
      '* `', datasets$portal, '`: [', datasets$name, ']',
      '(https://', datasets$portal, '/-/-/', datasets$id, ')',
      ' (', datasets$downloadCount, ' downloads)',
      sep = ''
    ),
    collapse = '\n'
  ))
}

plot.count <- function(variable, label, col = 1, ...) {
  log.max <- ceiling(log10(max(variable)))
  stripchart(log10(variable), method = 'jitter',
    pch = 21, col = NA, bg = adjustcolor(col, alpha.f = 0.2), xlim = c(0,log.max),
    axes = F, xlab = paste('Number of', label, 'owned by the user'),
    main = 'Each dot is a user', jitter = 1, ylim = c(0,2)
  )
  axis(1, at = c(0:log.max), labels = 10^(0:log.max))
}

build <- function(files = list.files()) {
  for (Rmd in grep('[.]Rmd$', files, value = T)){
    md <- sub('Rmd$', 'md', Rmd)
    figure <- sub('.Rmd$', '-figure', Rmd)

    # Remove the old figures.
    file.remove(c(paste(figure, list.files(figure), sep = '/'), figure))

    # Compile the markdown and the figures.
    knit(Rmd, md)

    # Rename the figure directory so we separate different figure directories.
    file.rename('figure', figure)
  }
}

