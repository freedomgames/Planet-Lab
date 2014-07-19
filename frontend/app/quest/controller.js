var questCtrlUtil = {
    upload: function($files, quest, S3) {
        S3.upload($files[0], 'quests', quest.id, 'uploads').then(
            function(iconUrl) {
                quest.icon_url = iconUrl;
        });
    }
};

planet_app.controller('QuestCtrl', [
    '$scope', '$stateParams', 'ResourceFactory', 'S3',
    function($scope, $stateParams, ResourceFactory, S3) {
        $scope.quest = ResourceFactory('quests').get({id: $stateParams.id})
        // have to wrap $scope.quest.$put in a new function as the promise
        // won't be back in time to do a $scope.save = $scope.quest.$put
        $scope.save = function() {$scope.quest.$put()};
        $scope.onFileSelect = function($files) {
            questCtrlUtil.upload($files, $scope.quest, S3);
        };
}]);

planet_app.controller('NewQuestCtrl', [
    '$scope', 'ResourceFactory', 'S3',
    function($scope, ResourceFactory, S3) {
        $scope.quest = new (ResourceFactory('quests'));
        $scope.save = function() {
            if ($scope.quest.id) {
                $scope.quest.$put();
            } else {
                $scope.quest.$save();
            }
        };
        $scope.onFileSelect = function($files) {
            if (! $scope.quest.id) {
                // We need an id to upload quest assets to S3
                $scope.quest.$save().then(function() {
                    questCtrlUtil.upload($files, $scope.quest, S3);
                });
            } else {
                questCtrlUtil.upload($files, $scope.quest, S3);
            }
        };
}]);
