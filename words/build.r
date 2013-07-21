library(ggplot2)
library(plyr)
library(knitr)
library(scales)
library(reshape2)

if (!('socrata' %in% ls())) {
  socrata <- read.csv('../socrata.csv', stringsAsFactors = F)
  socrata$createdAt <- as.Date(as.POSIXct(socrata$createdAt, origin = '1970-01-01'))
}

if (!('users' %in% ls())) {
  users <- read.csv('../users.csv', stringsAsFactors = F)
  users$profileLastModified <- as.Date(as.POSIXct(users$profileLastModified, origin = '1970-01-01'))
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

for (Rmd in grep('[.]Rmd$', list.files(), value = T)){
  md <- sub('Rmd$', 'md', Rmd)
  figure <- sub('.Rmd$', '-figure', Rmd)

  # Remove the old figures.
  file.remove(c(paste(figure, list.files(figure), sep = '/'), figure))

  # Compile the markdown and the figures.
  knit(Rmd, md)

  # Rename the figure directory so we separate different figure directories.
  file.rename('figure', figure)
  break
}
