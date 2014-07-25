planetApp.directive('plEditList', function() {
    return {
        restrict: 'E',
        scope: {list: '=list', listName: '@list'},
        templateUrl: 'static/common/edit_list_widget.html',
        link: function(scope) {
            if (scope.list === undefined) {
                // We are working with a new, unsaved object
                scope.list = [];
            }
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
