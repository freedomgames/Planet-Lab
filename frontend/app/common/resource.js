'use strict';

planetApp.factory('ResourceFactory', ['$resource', function($resource) {
    return function(resourceName) {
        return $resource(
            '/v1/:resourceName/:id',
            {resourceName: resourceName, id: '@id'},
            {
                put: {method: 'PUT'},
                save: {
                    method: 'POST',
                    url: '/v1/:resourceName\/.' // escape the trailing slash
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
                    query: {
                        method: 'GET',
                        url: '/v1/:parentName/:parentId/:childName\/.',
                        isArray: false
                    },
                    save: {
                        method: 'POST',
                        url: '/v1/:parentName/:parentId/:childName\/.',
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
                    url: '/v1/:resourceName/:id/:uploadName\/.',
                    isArray: false
                }
            }
        );
    };
}]);
