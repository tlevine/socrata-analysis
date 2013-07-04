library(ggplot2)
library(plyr)
library(knitr)
library(scales)
library(reshape2)

if (!('socrata' %in% ls())) {
  socrata <- read.csv('../socrata.csv', stringsAsFactors = F)
  socrata$createdAt <- as.Date(as.POSIXct(socrata$createdAt, origin = '1970-01-01'))
}

# Helpers
listify <- function(datasets) {
  paste(
    '<ul>',
    paste(
      '<li>',
        '<a href="https://', datasets$portal, '/-/-/', datasets$id, '">', datasets$name, '</a>',
        ' (', datasets$downloadCount, ' downloads)',
      '</li>', sep = ''
    ),
    '</ul>',  
    collapse = '\n'
  )
}

for (Rmd in grep('[.]Rmd$', list.files(), value = T)){
  md <- sub('Rmd$', 'md', Rmd)
  knit(Rmd, md)

  figure <- sub('.Rmd$', '-figure', Rmd)
  file.rename('figure', figure)
  break
}
