/**
 * File: current_user.js
 * Description: Contains a factory to return the current user's id
 * Dependencies: $http, $q
 * @ngInject
 *
 * @package Planet-Lab
 */

/* === Function Declaration === */
function CurrentUserFcty ($http, $q) {
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
        $http.put('/logout').then(function() {
            currentUserId = null;
            window.location = '/';
        });
    };

    return {getCurrentUserId: getCurrentUserId, logOut: logOut};
}

/* === Factory Declaration === */
angular.module('planetApp')
    .factory('CurrentUserFcty', CurrentUserFcty);
