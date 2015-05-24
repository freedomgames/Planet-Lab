/**
 * File: quest/controller.js
 * Description: Contains controllers for various aspects of the quest part of the site
 * Dependencies: $stateParams, ResourceFcty, S3Fcty, $state
 * @ngInject
 *
 * @package Planet-Lab
 */

/* === Function Declarations === */
function QuestCtrl ($stateParams, ResourceFcty, S3Fcty) {
    this.quest = ResourceFcty('quests').get({id: $stateParams.id})
    this.save = function() {this.quest.$put()};
    this.onFileSelect = function($files) {
        S3Fcty.upload($files[0], 'quests', this.quest.id, 'uploads').then(
            function(iconUrl) {
                quest.icon_url = iconUrl;
            });
    };
    this.deleteQuest = function() {this.quest.$delete()};
}

function QuestFormCtrl ($state, $stateParams, ResourceFcty, S3Fcty) {
    if ($state.is('quests.form')) {
        $state.go('quests.form.basic');
    }
    if ($stateParams.id) {
        this.quest = ResourceFcty('quests').get({id: $stateParams.id});
    } else {
        this.quest = new (ResourceFcty('quests'));
    }
    this.save = function() {
        if (this.quest.id) {
            this.quest.$put();
        } else {
            this.quest.$save();
        }
    };
    this.onFileSelect = function($files) {
        if (!this.quest.id) {
            // We need an id to upload quest assets to S3
            this.quest.$save().then(function(quest) {
                S3Fcty.upload($files[0], 'quests', quest.id, 'uploads').then(
                    function(iconUrl) {
                        quest.icon_url = iconUrl;
                    });
            });
        } else {
            S3Fcty.upload($files[0], 'quests', this.quest.id, 'uploads').then(
                function(iconUrl) {
                    quest.icon_url = iconUrl;
                });
        }
    };
}

/* === Controller Declarations === */
angular.module('planetApp')
    .controller('QuestCtrl', QuestCtrl)
    .controller('QuestFormCtrl', QuestFormCtrl);
