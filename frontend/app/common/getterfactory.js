planet_app.factory('GetterFactory', ['$resource', function ($resource) {
    return {
        getItem: function(resource, id) {
            return $resource( '/v1/' + resource + '/:id',  {},  {
                query: {
                    method:'GET', 
                    params: {
                        id: id
                    }
                }
            })
        }
    }
}]);
