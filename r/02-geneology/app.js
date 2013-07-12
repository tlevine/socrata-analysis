function Dataset(params) {
  this.portal = params.portal
  this.id = params.id
  this.name = params.name
  this.portals = []
  this.url = function(){
    return 'https://' + this.portal + '/-/-/' + this.id
  }
  this.add_derived_dataset = function(derived_params) {
    if (!(derived_params.portal in this.portals.map(function(portal){return portal.portal}))){
      dataset = new Dataset(derived_params)
      this.portals.push(dataset)
    }
    for (var i = 0; i < this.portals.length; i++) {
      if (this.portals[i].portal == this.portal) {
        if (derived_params.id === this.id) {
          this.portals[i].name = derived_params.name
        } else {
          this.portals[i].add_derived_dataset(derived_params)
        }
        break
      }
    }
  }
}


function GeneologyCtrl($scope, $http) {
  // Buttons
  $scope.next = function() {
    $scope.i++
  }
  $scope.prev = function() {
    $scope.i--
  }

  $http.get('geneology/873607.json').then(function(res){
    // Make Dataset objects
    canonical_dataset = new Dataset(res.data.source)
    for (var i = 0; i < res.data.datasets.length; i++) {
      canonical_dataset.add_derived_dataset(res.data.datasets[i])
    }

    window.c = canonical_dataset

    // Choose the current dataset
    $scope.canonical_datasets = [canonical_dataset]
    $scope.i = 0 // Current dataset

    $scope.d = function() {
      return $scope.canonical_datasets[$scope.i]
    }
 
  })
}
