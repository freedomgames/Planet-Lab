planet_app.factory('ResourceFactory', ['$resource', function($resource) {
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
planet_app.factory('S3ResourceFactory', ['$resource', function($resource) {
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
