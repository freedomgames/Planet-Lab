/**
 * File: resource.js
 * Description: Contains various factories for working with the database
 * Dependencies: $resource
 * @ngInject
 *
 * @package Planet-Lab
 */

/* === Function Declarations === */
function ResourceFcty ($resource) {
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
}

function ManyToOneResourceFcty ($resource) {
    return function(childName, parentName, parentLink) {
        return $resource(
            '/v1/:parentName/:parentId/:childName/:childId',
            {
                parentName: parentName,
                childName: childName,
                parentId: '@parentId',
                childId: '@childId'
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
}

function S3ResourceFcty ($resource) {
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
}

/* === Factory Declarations === */
angular.module('planetApp')
    .factory('ResourceFcty', ResourceFcty)
    .factory('ManyToOneResourceFcty', ManyToOneResourceFcty)
    .factory('S3ResourceFcty', S3ResourceFcty);
