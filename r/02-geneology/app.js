var MONTHS = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
]

angular.module('geneology', ['angular-table'])
  .controller('GeneologyCtrl', ['$scope', '$http', function($scope, $http) {
  // Buttons
  $http.get('geneology.json').then(function(res){
    $scope.tables = res.data.map(function(table){
      table.datasets = table.datasets.map(function(dataset) {
        var d = new Date()
        d.setTime(1000 * dataset.createdAt)
        dataset.prettyDate = MONTHS[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear()
        dataset.ncell = dataset.nrow * dataset.ncol
        dataset.ncopies = dataset.portals.length
        return dataset
      })
      return table
    })
  })
}])
