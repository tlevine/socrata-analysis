// http://stackoverflow.com/questions/979256/sorting-an-array-of-javascript-objects
var sortBy = function(field, reverse, primer){
   var key = function (x) {return primer ? primer(x[field]) : x[field]};
   return function (a,b) {
       var A = key(a), B = key(b);
       return ((A < B) ? -1 : (A > B) ? +1 : 0) * [-1,1][+!!reverse];                  
   }
}

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
  _load = function() {
    $http.get('geneology/' + $scope.tableIds[$scope.i][0] + '.json').then(function(res){
      $scope.table = res.data
      $scope.table.datasets = $scope.table.datasets.map(function(dataset) {
      $scope.mainPortal = $scope.tableIds[$scope.i][1]
        var d = new Date()
        d.setTime(1000 * dataset.createdAt)
        dataset.prettyDate = MONTHS[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear()
        dataset.ncell = dataset.nrow * dataset.ncol
        dataset.ncopies = dataset.portals.length
        dataset.mainPortal = $scope.tableIds[$scope.i][1] // Redundant but it works
        return dataset
      })
    })
  }

  $scope.handleRowSelection = function(row) {
    row.selected = true
  }

  $scope.next = function() {
    $scope.i++
    _load()
  }
  $scope.prev = function() {
    $scope.i--
    _load()
  }

  $http.get('geneology/index.json').then(function(res){
    // Choose the current dataset
    $scope.tableIds = res.data
    $scope.i = 2 // Current dataset
    _load()
  })
}])
