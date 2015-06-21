/**
 * File: frontent/app/app.js
 * Description: Defines the Angular module and configures the routes
 * Dependencies: ui-router, ngResource, angularFileUpload, $stateProvider, $urlRouterProvider
 * @ngInject
 *
 * @package Planet-Lab
 */

'use strict';

/* === Module Declaration === */
angular
    .module('planetApp', ['angularFileUpload', 'ngResource', 'ui.router'])
    .config(Config);

/* === Configuration === */
function Config ($stateProvider, $urlRouterProvider) {
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
                            controller: 'UserQuestsCtrl',
                            controllerAs: 'userQuests'
                        },
                        'missions': {
                            templateUrl: 'static/mission/mission-central.html',
                            controller: 'UserMissionsCtrl',
                            controllerAs: 'userMissions'
                        }
                    }
                })
            .state('user.profile', {
                url: '/profile',
                templateUrl: 'static/user/user-profile.html',
                controller: 'UserCtrl',
                controllerAs: 'user'
            })
            .state('user.settings', {
                url: '/settings',
                templateUrl: 'static/user/settings.html',
                controller: 'UserSettingsCtrl',
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
        // Help State
        .state('help', {
            url: '/help',
            templateUrl: 'static/help/help.html',
            controller: 'HelpCtrl',
            controllerAs: 'help'
        });
}
