var planetApp = angular.module('planetApp', [
        'ui.router', 'ngResource', 'xeditable', 'angularFileUpload']);

planetApp.config([
    '$controllerProvider', '$provide', '$compileProvider', '$stateProvider',
    '$urlRouterProvider', function($controllerProvider, $provide,
    $compileProvider, $stateProvider, $urlRouterProvider) {

    /* CODE FOR ASYNC MODULE LOADING */
    planetApp._controller = planetApp.controller;
    planetApp._service = planetApp.service;
    planetApp._factory = planetApp.factory;
    planetApp._directive = planetApp.directive;

    planetApp.controller = function( name, constructor ) {
        $controllerProvider.register( name, constructor );
        return(this);
    };

    planetApp.service = function( name, constructor ) {
        $provide.service( name, constructor );
        return(this);
    };

    planetApp.factory = function( name, factory ) {
        $provide.factory( name, factory );
        return(this);
    };

    planetApp.directive = function( name, factory ) {
        $compileProvider.directive( name, factory );
        return(this);
    };

    /* ROUTING */
    $urlRouterProvider.otherwise('/user/quests');

    $stateProvider
        .state('newQuest', {
            url: '/quests/new',
            templateUrl: 'static/quest/view.html',
            controller: 'NewQuestCtrl'
        })
        .state('quest', {
            url: '/quests/:id',
            templateUrl: 'static/quest/view.html',
            controller: 'QuestCtrl'
        })
        .state('userQuests', {
            url: '/user/quests',
            templateUrl: 'static/quest/list_view.html',
            controller: 'UsersQuestsCtrl'
        });
}]);
