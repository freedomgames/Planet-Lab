'use strict';

planetApp.factory('CurrentUser', ['$http', '$q', function($http, $q) {
    // Functions for caching and retrieving the current user's id.
    var currentUserId = null;

    var getCurrentUserId = function() {
        if (currentUserId !== null) {
            return $q.when(currentUserId);
        } else {
            var result = $q.defer();
            $http.get('/current-user').
                success(function(data) {
                    currentUserId = data.user_id;
                    result.resolve(currentUserId);
                }).
                error(function(data) {
                    result.reject(data);
                })
            return result.promise;
        }
    };

    var logOut = function() {
        currentUserId = null;
    };

    return {getCurrentUserId: getCurrentUserId, logOut: logOut};
}]);
