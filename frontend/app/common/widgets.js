planet_app.directive('plEditList', function() {
    return {
        restrict: 'E',
        scope: {list: '='},
        templateUrl: 'static/common/edit_list_widget.html',
        link: function(scope) {
            scope.updateArrayItem = function($event, $index) {
                scope.list[$index] = $event.target.value;
            };
            scope.deleteArrayItem = function($index) {
                scope.list.splice($index, 1);
            };
            scope.newArrayItem = function() {
                scope.list.push('');
            };
        }
}})
