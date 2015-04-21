var missionCtrlUtil = {
    upload: function($files, mission, S3) {
        S3.upload($files[0], 'missions', mission.id, 'uploads');
    }
};

planetApp.controller('MissionCtrl', [
    '$scope', '$stateParams', 'ResourceFactory', 'S3', 
    function($scope, $stateParams, ResourceFactory, S3 ) {
        $scope.mission = ResourceFactory('missions').get({id: $stateParams.id})
        // have to wrap $scope.quest.$put in a new function as the promise
        // won't be back in time to do a $scope.save = $scope.quest.$put
        $scope.save = function() {$scope.mission.$put()};
        $scope.onFileSelect = function($files) {
            questCtrlUtil.upload($files, $scope.mission, S3);
        };
}]);

planetApp.controller('NewMissionCtrl', [
    '$scope', 'ResourceFactory', 'S3',
    function($scope, ResourceFactory, S3) {
        $scope.missions = new (ResourceFactory('missions'));
        $scope.save = function() {
            if ($scope.missions.id) {
                $scope.missions.$put();
            } else {
                $scope.missions.$save();
            }
        };
        $scope.onFileSelect = function($files) {
            if (! $scope.missions.id) {
                // We need an id to upload quest assets to S3
                $scope.missions.$save().then(function() {
                    missionCtrlUtil.upload($files, $scope.missions, S3);
                });
            } else {
                missionCtrlUtil.upload($files, $scope.missions, S3);
            }
        };
}]);

planetApp.controller('UsersQuestsCtrl', [
    '$scope', '$stateParams', 'CurrentUser', 'ManyToOneResourceFactory',
    function($scope, $stateParams, CurrentUser, ManyToOneResourceFactory) {
        CurrentUser.getCurrentUserId().then(function(userId) {
            $scope.missions = ManyToOneResourceFactory('missions', 'users').query(
                {parentId: userId});
        });
}]);
