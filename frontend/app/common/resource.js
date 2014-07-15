planet_app.factory('ResourceFactory', [
    '$resource', '$stateParams', function($resource, $stateParams) {
        return function(resourceName) {
            return $resource(
                '/v1/:resourceName/:id',
                {resourceName: resourceName, id: $stateParams.id},
                {put: {method: 'PUT'}}
            );
        };
}]);
