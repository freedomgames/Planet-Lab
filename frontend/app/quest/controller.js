var updateScope = function($scope) {
    // Set common functions required by views of both controllers
    $scope.updateArrayItem = function(name, $event, $index) {
        $scope.quest[name][$index] = $event.target.value;
    };
    $scope.deleteArrayItem = function(name, $index) {
        $scope.quest[name].splice($index, 1);
    };
    $scope.newArrayItem = function(name) {
        $scope.quest[name].push('');
    };
};

planet_app.controller('QuestCtrl', [
    '$scope', '$stateParams', 'ResourceFactory',
    function($scope, $stateParams, ResourceFactory) {
        $scope.quest = ResourceFactory('quests').get({id: $stateParams.id})
        // have to wrap $scope.quest.$put in a new function as the promise
        // won't be back in time to do a $scope.save = $scope.quest.$put
        $scope.save = function() {$scope.quest.$put()};
        updateScope($scope);
}]);

planet_app.controller('NewQuestCtrl', [
    '$scope', 'ResourceFactory', function($scope, ResourceFactory) {
        $scope.quest = new (ResourceFactory('quests'));
        $scope.save = function() {
            if ($scope.quest.id) {
                $scope.quest.$put();
            } else {
                $scope.quest.$save();
            }
        };
        updateScope($scope);
}]);
