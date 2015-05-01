var userCtrlUtil = {
    upload: function($files, user, S3) {
        S3.upload($files[0], 'users', user.id, 'avatar').then(
            function(avatar_url) {
                user.avatar_url = avatar_url;
        });
    }
};

planetApp.controller('LogOutCtrl', [
    '$scope', 'CurrentUser', function($scope, CurrentUser) {
        this.logOut = CurrentUser.logOut;
}]);

planetApp.controller('UsersCtrl', [
    '$scope', '$stateParams', 'ResourceFactory', 'S3', 'CurrentUser',
    function($scope, $stateParams, ResourceFactory, S3, CurrentUser) {
        CurrentUser.getCurrentUserId().then(function(id) {
            this.user = ResourceFactory('users').get({id: id})
        }.bind(this));
        // have to wrap $scope.quest.$put in a new function as the promise
        // won't be back in time to do a $scope.save = $scope.quest.$put
        this.save = function() {this.user.$put()};
        this.onFileSelect = function($files) {
            userCtrlUtil.upload($files, this.user, S3);
        };
}]);

planetApp.controller('UsersQuestsCtrl', [
    '$scope', 'ManyToOneResourceFactory', 'CurrentUser',
    function($scope, ManyToOneResourceFactory, CurrentUser) {
        CurrentUser.getCurrentUserId().then(function(id) {
            this.quests = ManyToOneResourceFactory('quests', 'users').query({parentId: id});
        }.bind(this));
}]);

planetApp.controller('UsersMissionsCtrl', [
    '$scope', 'CurrentUser', 'ManyToOneResourceFactory',
    function($scope, CurrentUser, ManyToOneResourceFactory) {
        CurrentUser.getCurrentUserId().then(function(id) {
            this.missions = ManyToOneResourceFactory('missions', 'users').query({parentId: id});
        }.bind(this));
}]);

planetApp.controller('UsersSettingsCtrl', [
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
