planetApp.controller('LogOutCtrl', [
    '$scope', 'CurrentUser', function($scope, CurrentUser, S3) {
        $scope.logOut = CurrentUser.logOut;
}]);
