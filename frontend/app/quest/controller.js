planet_app.controller('QuestCtrl', [
    '$scope', '$stateParams', 'ResourceFactory',
    function($scope, $stateParams, ResourceFactory) {
        $scope.quest = ResourceFactory('quests').get({id: $stateParams.id})
        // have to wrap $scope.quest.$put in a new function as the promise
        // won't be back in time to do a $scope.save = $scope.quest.$put
        $scope.save = function() {$scope.quest.$put()};
}]);

planet_app.controller('NewQuestCtrl', [
    '$scope', 'ResourceFactory', function($scope, ResourceFactory) {
        $scope.quest = new (ResourceFactory('quests'));
        $scope.save = function() {
            if ($scope.quest.id) {
                $scope.quest.$put();
            } else {
                // place-holder values for inquiry_questions and video_links
                // until that part of the UI is supplying them.
                $scope.quest.inquiry_questions = [];
                $scope.quest.video_links = [];
                $scope.quest.$save();
            }
        };
}]);
