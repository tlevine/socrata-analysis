function GeneologyCtrl($scope, $http) {
  // Buttons
  _load = function() {
    $http.get('geneology/' + $scope.tableIds[$scope.i] + '.json').then(function(res){
      $scope.table = res.data
    })
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
    $scope.i = 0 // Current dataset
    _load()
  })
}
