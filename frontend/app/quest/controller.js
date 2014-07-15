planet_app.controller('QuestCtrl', [
    '$scope', 'ResourceFactory', function ($scope, ResourceFactory) {
        $scope.quest = ResourceFactory('quests').get();
}]);
