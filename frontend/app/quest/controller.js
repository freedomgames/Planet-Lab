planet_app.controller('QuestCtrl', ['$scope', '$resource', '$stateParams', 'GetterFactory', function ($scope, $resource, $stateParams, GetterFactory) {
    $scope.quest = GetterFactory.getItem('quests', $stateParams.id).query();
}]);
