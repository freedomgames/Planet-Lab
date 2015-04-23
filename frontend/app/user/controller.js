var userCtrlUtil = {
    upload: function($files, user, S3) {
        S3.upload($files[0], 'users', user.id, 'avatar').then(
            function(avatar_url) {
                console.log(avatar_url)
                user.avatar_url = avatar_url;
        });
    }
};

planetApp.controller('LogOutCtrl', [
    '$scope', 'CurrentUser', function($scope, CurrentUser, S3) {
        this.logOut = CurrentUser.logOut;
}]);

planetApp.controller('UsersCtrl', [
    '$scope', '$stateParams', 'ResourceFactory', 'S3', 'curr',
    function($scope, $stateParams, ResourceFactory, S3, curr ) {
        this.user = ResourceFactory('users').get({id: curr})
        // have to wrap $scope.quest.$put in a new function as the promise
        // won't be back in time to do a $scope.save = $scope.quest.$put
        this.save = function() {this.user.$put()};
        this.onFileSelect = function($files) {
            userCtrlUtil.upload($files, this.user, S3);
        };
}]);

planetApp.controller('UsersQuestsCtrl', [
    '$scope', '$stateParams', 'CurrentUser', 'ManyToOneResourceFactory', 'quests',
    function($scope, $stateParams, CurrentUser, ManyToOneResourceFactory, quests) {
        this.quests = quests || [];
}]);

planetApp.controller('UsersMissionsCtrl', [
    '$scope', '$stateParams', 'CurrentUser', 'ManyToOneResourceFactory', 'missions',
    function($scope, $stateParams, CurrentUser, ManyToOneResourceFactory, missions) {
        this.missions = missions || [];
}]);
