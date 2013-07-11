function Dataset(canonical_portal, canonical_id, canonical_name) {
  this.portal = canonical_portal
  this.id = canonical_id
  this.name = canonical_name
  this.portals = {}
  this.url = function(){
    return 'https://' + this.portal + '/-/-/' + this.id
  }
  this.add_derived_dataset = function(derived_portal, derived_id, derived_name) {
    if (!(derived_portal in this.portals)){
      this.portals[derived_portal] = new Dataset(derived_portal, canonical_id, canonical_name)
    }
    if (canonical_id === derived_id) {
      this.portals[derived_portal].name = derived_name
    } else {
      this.portals[derived_portal].add_derived_dataset(derived_portal, derived_id, derived_name)
    }
  }
}

greenbook = new Dataset('explore.data.gov', '5gah-bvex', 'U.S. Overseas Loans and Grants (Greenbook)')
greenbook.add_derived_dataset('data.hawaii.gov', '5gah-bvex', 'U.S. Overseas Loans and Grants (Greenbook)')

function TodoCtrl($scope) {
  $scope.todos = [
    {text:'learn angular', done:true},
    {text:'build an angular app', done:false}];
 
  $scope.addTodo = function() {
    $scope.todos.push({text:$scope.todoText, done:false});
    $scope.todoText = '';
  };
 
  $scope.remaining = function() {
    var count = 0;
    angular.forEach($scope.todos, function(todo) {
      count += todo.done ? 0 : 1;
    });
    return count;
  };
 
  $scope.archive = function() {
    var oldTodos = $scope.todos;
    $scope.todos = [];
    angular.forEach(oldTodos, function(todo) {
      if (!todo.done) $scope.todos.push(todo);
    });
  };
}
