function Dataset(params) {
  this.portal = params.portal
  this.id = params.id
  this.name = params.name
  this.portals = []
  this.url = function(){
    return 'https://' + this.portal + '/-/-/' + this.id
  }
  this.add_derived_dataset = function(derived_params) {
    if (!(derived_params.portal in this.portals.map(function(portal){portal.portal}))){
      dataset = new Dataset(derived_params.portal, this.id, this.name)
      this.portals.push(dataset)
    }
    for (var i = 0; i < this.portals.length; i++) {
      if (this.portals[i].portal == this.portal) {
        if (derived_params.id === this.id) {
          this.portals[i].name = derived_params.name
        } else {
          this.portals[i].add_derived_dataset(derived_params.portal, derived_params.id, derived_params.name)
        }
        break
      }
    }
  }
}


function GeneologyCtrl($scope, $http) {
  var canonical_dataset = $http.get('geneology/873607.json').then(function(res){
    canonical_dataset = new Dataset(res.data.source)
    res.data.datasets.map(function(dataset){
      canonical_dataset.add_derived_dataset(dataset)
    })
    console.log(canonical_dataset)
    return canonical_dataset
  })
  window.c = canonical_dataset

  $scope.canonical_datasets = [canonical_dataset]
  $scope.i = 0 // Current dataset
 
  $scope.next = function() {
    $scope.i++
  }
  $scope.prev = function() {
    $scope.i--
  }

  $scope.d = function() {
    return $scope.canonical_datasets[$scope.i]
  }
 
}
