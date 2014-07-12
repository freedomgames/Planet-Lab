planet_app.controller('QuestCtrl', ['$scope', '$resource', '$stateParams', function ($scope, $resource, $stateParams) {
    quest = $resource( '/v1/quests/:id',  {},  {
                query: {
                    method:'GET',
                    params: {
                        id: $stateParams.id
                    }
                }
            });

    $scope.quest = quest.query();
}]);
