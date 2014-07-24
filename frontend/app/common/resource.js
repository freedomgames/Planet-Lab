'use strict';

planetApp.factory('ResourceFactory', ['$resource', function($resource) {
    return function(resourceName) {
        return $resource(
            '/v1/:resourceName/:id',
            {resourceName: resourceName, id: '@id'},
            {
                put: {method: 'PUT'},
                query: {
                    method: 'GET',
                    isArray: true,
                    transformResponse: function(data) {
                        // The backend returns a response like:
                        // {quests: [{name: ...}, {...}]}
                        // due to security issues with returning top-level
                        // JSON Arrays in a callabck.  We flatten the
                        // object into an array here for convenience.
                        return angular.fromJson(data)[resourceName];
                    }
                }
            }
        );
    };
}]);
planetApp.factory('ManyToOneResourceFactory', [
    '$resource', function($resource) {
        return function(childName, parentName, parentLink) {
            return $resource(
                '/v1/:parentName/:parentId/:childName/:childId',
                {
                    parentName: parentName,
                    childName: childName,
                    parentId: '@' + parentLink,
                    childId: '@id'
                },
                {
                    put: {method: 'PUT'},
                    query: {
                        method: 'GET',
                        isArray: true,
                        transformResponse: function(data) {
                            // The backend returns a response like:
                            // {quests: [{name: ...}, {...}]}
                            // due to security issues with returning top-level
                            // JSON Arrays in a callabck.  We flatten the
                            // object into an array here for convenience.
                            return angular.fromJson(data)[childName];
                        }
                    }
                }
            );
    };
}]);
planetApp.factory('S3ResourceFactory', ['$resource', function($resource) {
    return function(resourceName) {
        return $resource(
            '/v1/:resourceName/:id/:uploadName/:fileName',
            {resourceName: resourceName, id: '@id'},
            {
                query: {
                    method: 'GET',
                    isArray: true,
                    transformResponse: function(data) {
                        // The backend returns a response like:
                        // {quests: [{name: ...}, {...}]}
                        // due to security issues with returning top-level
                        // JSON Arrays in a callabck.  We flatten the
                        // object into an array here for convenience.
                        return angular.fromJson(data).assets;
                    }
                }
            }
        );
    };
}]);
