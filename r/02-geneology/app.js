// http://stackoverflow.com/questions/979256/sorting-an-array-of-javascript-objects
var sortBy = function(field, reverse, primer){
   var key = function (x) {return primer ? primer(x[field]) : x[field]};
   return function (a,b) {
       var A = key(a), B = key(b);
       return ((A < B) ? -1 : (A > B) ? +1 : 0) * [-1,1][+!!reverse];                  
   }
}

function GeneologyCtrl($scope, $http) {
  // Buttons
  _load = function() {
    $http.get('geneology/' + $scope.tableIds[$scope.i][0] + '.json').then(function(res){
      $scope.table = res.data
      $scope.mainPortal = $scope.tableIds[$scope.i][1]
      $scope.table.datasets = $scope.table.datasets.sort(sortBy($scope.sortField, $scope.sortReverse))
    })
  }

  $scope.sortField = 'downloadCount'
  $scope.sortReverse = false

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
}
