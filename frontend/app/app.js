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
            .state('quests.new', {
                abstract: true,
                url: '/new',
                templateUrl: 'static/quest/new-quest.html',
                controller: 'NewQuestCtrl',
                controllerAs: 'questNew'
            })
                .state('quests.new.basic', {
                    url: '/basic-info',
                    templateUrl: 'static/quest/new/basic-info.html',
                })
                .state('quests.new.activity', {
                    url: '/activity',
                    templateUrl: 'static/quest/new/activity-details.html',
                })
                .state('quests.new.teachers', {
                    url: '/teacher',
                    templateUrl: 'static/quest/new/for-teachers.html',
                })
                .state('quests.new.review', {
                    url: '/review',
                    templateUrl: 'static/quest/new/review-quest.html',
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
            .state('missions.new', {
                url: '/new',
                templateUrl: 'static/mission/new-mission.html',
                controller: 'NewMissionCtrl',
                controllerAs: 'missionNew'
            })
                .state('missions.new.basic', {
                    url: '/basic-info',
                    templateUrl: 'static/mission/new/basic-info.html',
                })
                .state('missions.new.quests', {
                    url: '/add-quests',
                    templateUrl: 'static/mission/new/add-quests.html',
                })
                .state('missions.new.badges', {
                    url: '/badges',
                    templateUrl: 'static/mission/new/badges.html',
                })
                .state('missions.new.review', {
                    url: '/review',
                    templateUrl: 'static/mission/new/review-mission.html',
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


