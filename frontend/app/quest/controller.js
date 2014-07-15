planet_app.controller('QuestCtrl', ['$scope', '$stateParams', 'GetterFactory', function ($scope, $stateParams, GetterFactory) {
    $scope.quest = GetterFactory.getItem('quests', $stateParams.id).query();
}]);
