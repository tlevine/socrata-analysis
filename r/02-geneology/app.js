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

angular.module('geneology', ['angular-table', '$strap.directives'])
  .controller('GeneologyCtrl', ['$scope', '$http', function($scope, $http) {
  // Buttons
  _load = function(i) {
    $http.get('geneology/' + $scope.tableIds[i][0] + '.json').then(function(res){
      $scope.table = res.data
      $scope.table.datasets = $scope.table.datasets.map(function(dataset) {
      $scope.mainPortal = $scope.tableIds[i][1]
        var d = new Date()
        d.setTime(1000 * dataset.createdAt)
        dataset.prettyDate = MONTHS[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear()
        dataset.ncell = dataset.nrow * dataset.ncol
        dataset.ncopies = dataset.portals.length
        dataset.mainPortal = $scope.tableIds[i][1] // Redundant but it works
        return dataset
      })
    })
  }

  $http.get('geneology/index.json').then(function(res){
    // Choose the current dataset
    $scope.tableIds = res.data
    $scope.dropdown = $scope.tableIds.map(function(tableId) {
      return {
        "text": tableId[2],
        "href": "_load(" + tableId[0] + ")"
      }
    })
    _load(2)
  })
}])
