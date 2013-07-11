function Dataset(canonical_portal, canonical_id, canonical_name) {
  this.portal = canonical_portal
  this.id = canonical_id
  this.name = canonical_name
  this.portals = []
  this.url = function(){
    return 'https://' + this.portal + '/-/-/' + this.id
  }
  this.add_derived_dataset = function(derived_portal, derived_id, derived_name) {
    if (!(derived_portal in this.portals.map(function(portal){portal.portal}))){
      dataset = new Dataset(derived_portal, this.id, this.name)
      this.portals.push(dataset)
    }
    for (var i = 0; i < this.portals.length; i++) {
      if (this.portals[i].portal == this.portal) {
        if (derived_id === this.id) {
          this.portals[i].name = derived_name
        } else {
          this.portals[i].add_derived_dataset(derived_portal, derived_id, derived_name)
        }
        break
      }
    }
  }
}


function GeneologyCtrl($scope) {
  greenbook = new Dataset('explore.data.gov', '5gah-bvex', 'U.S. Overseas Loans and Grants (Greenbook)')
  greenbook.add_derived_dataset('data.hawaii.gov', '5gah-bvex', 'U.S. Overseas Loans and Grants (Greenbook)')

  $scope.canonical_datasets = [greenbook]
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
