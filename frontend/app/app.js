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
            template: '<ui-view/>',
            resolve: {
                curr: function (CurrentUser) {
                   return CurrentUser.getCurrentUserId();
                }
            }
        })
            .state('user.dashboard', {
                abstract: true,
                templateUrl: 'static/user/dashboard.html',
                resolve: {
                    quests: function (curr, ManyToOneResourceFactory) {
                        return ManyToOneResourceFactory('quests', 'users').query({parentId: curr}).$promise;
                    },
                    missions: function (curr, ManyToOneResourceFactory) {
                        return ManyToOneResourceFactory('missions', 'users').query({parentId: curr}).$promise;
                    }
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
                controllerAs: 'missionForm',
                resolve: {
                    curr: function (CurrentUser) {
                       return CurrentUser.getCurrentUserId();
                    }
                }
            })
                .state('missions.form.basic', {
                    url: '/basic-info',
                    templateUrl: 'static/mission/form/basic-info.html',
                })
                .state('missions.form.quests', {
                    url: '/add-quests',
                    templateUrl: 'static/mission/form/add-quests.html',
                })
                .state('missions.form.badges', {
                    url: '/badges',
                    templateUrl: 'static/mission/form/badges.html',
                })
                .state('missions.form.review', {
                    url: '/review',
                    templateUrl: 'static/mission/form/review-mission.html',
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
                controllerAs: 'organizationNew'
            })
                .state('organizations.new.basic', {
                    url: '/basic-info',
                    templateUrl: 'static/organization/new/basic-info.html',
                })
}]);


