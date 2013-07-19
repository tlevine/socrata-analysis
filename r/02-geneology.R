library(ggplot2)
library(scales)

d <- t(matrix(c(
  71042, 48786, 3505, 732,
  5466, 4145, 1403, 537,
  97391, 46973, 6798, 5269,
  1245049, 6013, 103023, 136,
  13215, 3206, 2880, 268,
  41372, 16940, 57998, 50398,
  374813, 206, 10956, 24,
  80515, 9037, 7254, 1089,
  281339, 7268, 10741, 633,
  1455933, 1351374, 26485, 10398
), 4))
dataset.names <- c(
  'TIF Projection Reports',
  'FEC Contributions',
  'Federal Data Center',
  'RadNet Laboratory Analysis',
  'TIF Balance Sheets',
  '311 Service Requests',
  'Summary of IBRD Active',
  'Major Contract Awards',
  'IDA Statement of Credits',
  'White House Visitor'
)
top.datasets <- data.frame(
  name = rep(dataset.names, 4),
  variable = factor(rep(c('Hits','Downloads'), each = 20)),
  scope = factor(rep(c('Whole family','Source only'), each = 10)),
  value = c(d[,1], d[,2], d[,3], d[,4])
)
rm(d)
rm(dataset.names)

plot.family <- function(variable.name) {
  p <- ggplot(subset(top.datasets, variable == variable.name)) +
    aes(y = name, x = value, color = scope) +
    scale_x_log10('Value', labels = comma, breaks = 10^c(2:9)) +
    scale_y_discrete('Dataset') +
    ggtitle(paste(variable.name, 'by dataset family')) +
    geom_line(aes(group = name), color = 'black') +
    geom_point(aes(size = 100))
  png(paste0('02-geneology/', variable.name, '.png'),
    width = 840, height = 610, res = 100)
  print(p)
  dev.off()
}

for (v in levels(top.datasets$variable)) {
  plot.family(v)
}
