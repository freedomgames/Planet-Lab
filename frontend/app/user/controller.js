/**
 * File: user/controller.js
 * Description: Contains various controllers for user-based functionality on the site
 * Dependencies: CurrentUserFcty, $stateParams, ResourceFcty, S3Fcty
 * @ngInject
 *
 * @package Planet-Lab
 */

/* === Function Declarations === */
function UserLogoutCtrl (CurrentUserFcty) {
    this.logOut = CurrentUserFcty.logOut;
}

function UserCtrl ($stateParams, CurrentUserFcty, ResourceFcty, S3Fcty) {
    CurrentUserFcty.getCurrentUserId().then(function(id) {
        this.user = ResourceFcty('users').get({id: id})
    }.bind(this));
    this.save = function() {this.user.$put()};
    this.onFileSelect = function($files) {
        S3Fcty.upload($files[0], 'users', this.user.id, 'avatar').then(
            function(avatar_url) {
                this.user.avatar_url = avatar_url.replace(' ', '%20');
            }.bind(this));
    };
}

function UserQuestsCtrl (CurrentUserFcty, ManyToOneResourceFcty) {
    CurrentUserFcty.getCurrentUserId().then(function(id) {
        this.quests = ManyToOneResourceFcty('quests', 'users').query({parentId: id});
    }.bind(this));
}

function UserMissionsCtrl (CurrentUserFcty, ManyToOneResourceFcty) {
    CurrentUserFcty.getCurrentUserId().then(function(id) {
        this.missions = ManyToOneResourceFcty('missions', 'users').query({parentId: id});
    }.bind(this));
}

function UserSettingsCtrl ($stateParams, CurrentUserFcty, ResourceFcty, S3Fcty) {
    CurrentUserFcty.getCurrentUserId().then(function(id) {
        this.user = ResourceFcty('users').get({id: id})
    }.bind(this));
    this.save = function() {this.user.$put()};
    this.onFileSelect = function($files) {
        S3Fcty.upload($files[0], 'users', this.user.id, 'avatar').then(
            function(avatar_url) {
                this.user.avatar_url = avatar_url;
            }.bind(this));
    };
}

/* === Controller Declarations === */
angular.module('planetApp')
    .controller('UserLogoutCtrl', UserLogoutCtrl)
    .controller('UserCtrl', UserCtrl)
    .controller('UserQuestsCtrl', UserQuestsCtrl)
    .controller('UserMissionsCtrl', UserMissionsCtrl)
    .controller('UserSettingsCtrl', UserSettingsCtrl);
