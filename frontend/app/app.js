var planetApp = angular.module('planetApp', [
        'ui.router', 'ngResource', 'angularFileUpload']);

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
    $urlRouterProvider.otherwise('/user/dashboard');

    $stateProvider
        // Quests State
        .state('quests', {
            abstract: true,
            url: '/quests',
            template: '<ui-view/>'
        })
            .state('quests.quest', {
                url: '/:id',
                templateUrl: 'static/quest/view.html',
                controller: 'QuestCtrl',
                controllerAs: 'quest'
            })
            .state('quests.form', {
                url: '/form/:id',
                templateUrl: 'static/quest/quest-form.html',
                controller: 'QuestFormCtrl',
                controllerAs: 'questForm'
            })
                .state('quests.form.basic', {
                    url: '/basic-info',
                    templateUrl: 'static/quest/form/basic-info.html'
                })
                .state('quests.form.activity', {
                    url: '/activity',
                    templateUrl: 'static/quest/form/activity-details.html'
                })
                .state('quests.form.teachers', {
                    url: '/teacher',
                    templateUrl: 'static/quest/form/for-teachers.html'
                })
                .state('quests.form.review', {
                    url: '/review',
                    templateUrl: 'static/quest/form/review-quest.html'
                })
        // User State
        .state('user', {
            abstract: true,
            url: '/user',
            template: '<ui-view/>'
        })
            .state('user.dashboard', {
                abstract: true,
                templateUrl: 'static/user/dashboard.html',
                resolve: {
                }
            })
                .state('user.dashboard.views', {
                    url: '/dashboard',
                    views: {
                        'quests': {
                            templateUrl: 'static/quest/quest-central.html',
                            controller: 'UsersQuestsCtrl',
                            controllerAs: 'userQuests'
                        },
                        'missions': {
                            templateUrl: 'static/mission/mission-central.html',
                            controller: 'UsersMissionsCtrl',
                            controllerAs: 'userMissions'
                        }
                    }
                })
            .state('user.profile', {
                url: '/profile',
                templateUrl: 'static/user/user-profile.html',
                controller: 'UsersCtrl',
                controllerAs: 'users'
            })
            .state('user.settings', {
                url: '/settings',
                templateUrl: 'static/user/settings.html',
                controller: 'UsersSettingsCtrl',
                controllerAs: 'userSettings'
            })
        // Missions State
        .state('missions', {
            abstract: true,
            url: '/missions',
            template: '<ui-view/>'
        })
        .state('missions.mission', {
                url: '/:id',
                templateUrl: 'static/mission/view.html',
                controller: 'MissionCtrl',
                controllerAs: 'mission'
            })
            .state('missions.form', {
                url: '/form/:id',
                templateUrl: 'static/mission/mission-form.html',
                controller: 'MissionFormCtrl',
                controllerAs: 'missionForm'
            })
                .state('missions.form.basic', {
                    url: '/basic-info',
                    templateUrl: 'static/mission/form/basic-info.html',
                })
                .state('missions.form.quests', {
                    url: '/add-quests',
                    templateUrl: 'static/mission/form/add-quests.html',
                })
        // Organizations State
        .state('organizations', {
            abstract: true,
            url: '/organizations',
            template: '<ui-view/>'
        })
            .state('organizations.new', {
                url: '/new',
                templateUrl: 'static/organization/new-organization.html',
                controller: 'NewOrganizationCtrl',
                controllerAs: 'orgNew'
            })
                .state('organizations.new.basic', {
                    url: '/basic-info',
                    templateUrl: 'static/organization/new/basic-info.html',
                })

        // Help State
        .state('help', {
            url: '/help',
            templateUrl: 'static/help/help.html',
            controller: 'HelpCtrl',
            controllerAs: 'help'
        });
        
}]);
