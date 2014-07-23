'use strict';

planetApp.factory('ResourceFactory', ['$resource', function($resource) {
    return function(resourceName) {
        return $resource(
            '/v1/:resourceName/:id',
            {resourceName: resourceName, id: '@id'},
            {
                put: {method: 'PUT'},
                query: { method: 'GET', isArray: false}
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
                    query: {method: 'GET', isArray: false}
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
                    url: '/v1/:resourceName/:id/:uploadName\/.',
                    isArray: false
                }
            }
        );
    };
}]);
