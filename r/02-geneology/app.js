function Dataset(params) {
  this.portal = params.portal
  this.id = params.id
  this.name = params.name
  this.description = params.description
  this.nrow = params.nrow
  this.ncol = params.ncol
  this.createdAt = params.createdAt
  this.modifyingViewUid = params.modifyingViewUid
  this.viewCount = params.viewCount

  this.portals = []
  this.filtered_views = []
  this.url = function(){
    return 'https://' + this.portal + '/-/-/' + this.id
  }

  this.update = function(new_params){
    for (param in {"portal":null, "id":null, "name":null, "description":null, "nrow":null, "ncol":null, "createdAt":null, "viewCount":null}){
      if (typeof(this[param]) !== 'undefined'){
        this[param] = new_params[param]
      }
    }
    for (list in {"portals":null, "filtered_views":null}) {
      if (typeof(this[list]) !== 'undefined'){
        this[list] = this[list].concat(new_params[list])
      }
    }
  }

  this.add_derived_dataset = function(derived_params) {
    var dataset = new Dataset(derived_params)

    // Add the portal if it isn't already there.
    if (this.portals.map(function(portal){return portal.portal}).indexOf(dataset.portal) === -1){
      this.portals.push(dataset)
    }

    for (var i = 0; i < this.portals.length; i++) {
      if (this.portals[i].portal == this.portal) {
        if (derived_params.is_filtered_view) {
          // Add the dataset as a filtered view if it is a filtered view.
          this.portals[i].filtered_views.push(dataset)
        } else {
          // Set the portal properties to this one if it is the data portal root
          this.portals[i].update(derived_params)
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
      var canonical_dataset = new Dataset(res.data.source)
      for (var i = 0; i < res.data.datasets.length; i++) {
        canonical_dataset.add_derived_dataset(res.data.datasets[i])
      }
      $scope.canonical_dataset = canonical_dataset
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
