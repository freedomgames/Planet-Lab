planet_app.controller('QuestCtrl', [
    '$scope', 'ResourceFactory', function ($scope, ResourceFactory) {
        $scope.quest = ResourceFactory('quests').get();
        $scope.update = function() {
            if ($scope.questForm.$valid) {
                $scope.quest.$put();
            }
        };
}]);
