function Dataset(params) {
  this.portal = params.portal
  this.id = params.id
  this.name = params.name
  this.portals = []
  this.filtered_views = []
  this.url = function(){
    return 'https://' + this.portal + '/-/-/' + this.id
  }
  this.add_derived_dataset = function(derived_params) {
    if (this.portals.map(function(portal){return portal.portal}).indexOf(derived_params.portal) === -1){
      dataset = new Dataset({
        "portal": derived_params.portal,
        "id": this.id,
        "name": this.name
      })
      this.portals.push(dataset)
    }
    for (var i = 0; i < this.portals.length; i++) {
      if (this.portals[i].portal == this.portal) {
        if (derived_params.id === this.id) {
          this.portals[i].name = derived_params.name
        } else {
          derived_dataset = new Dataset(derived_params)
          this.portals[i].filtered_views.push(derived_dataset)
        }
        break
      }
    }
  }
}


function GeneologyCtrl($scope, $http) {
  // Buttons
  _load = function() {
    $http.get('geneology/' + $scope.tableIds[$scope.i] + '.json').then(function(res){
      // Make Dataset objects
      $scope.canonical_dataset = new Dataset(res.data.source)
      for (var i = 0; i < res.data.datasets.length; i++) {
        $scope.canonical_dataset.add_derived_dataset(res.data.datasets[i])
      }
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
