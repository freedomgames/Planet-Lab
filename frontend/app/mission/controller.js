/**
 * File: mission/controller.js
 * Description: Contains the controllers for various parts of the mission section of the site
 * Dependencies: $stateParams, ResourceFcty, S3Fcty, ManyToOneResourceFcty, $state, CurrentUserFcty
 * @ngInject
 *
 * @package Planet-Lab
 */

/* === Function Declarations === */
function MissionCtrl ($stateParams, ResourceFcty, S3Fcty ) {
    this.mission = ResourceFcty('missions').get({id: $stateParams.id})
}

function MissionFormCtrl ($state, $stateParams, CurrentUserFcty, ManyToOneResourceFcty, ResourceFcty, S3Fcty) {
    if ($state.is('missions.form')) {
        $state.go('missions.form.basic');
    }

    CurrentUser.getCurrentUserId().then(function(id) {
        this.user_quests = ManyToOneResourceFcty('quests', 'users').query({parentId: id});
    });
    this.quests = [""];
    if ($stateParams.id) {
        this.mission = ResourceFcty('missions').get({id: $stateParams.id});
    } else {
        this.mission = new (ResourceFcty('missions'));
    }
    this.save = function() {
        if (this.mission.id) {
            this.mission.$put();
        } else {
            this.mission.$save();
        }
    };
    this.addNewQuest = function () {
        this.quests.push("");
    };
    this.iterateQuests = function () {
        for (var i = 0; i < this.quests.length; i++) {
            this.missionLink = new (ManyToOneResourceFcty('quests', 'missions'));
            var id = this.quests[i];
            this.missionLink.$put({childId: id, parentId: this.mission.id}); 
        }
    };
    this.saveQuests = function () {
        if (! this.mission.id) {
            this.mission.$save().then(this.iterateQuests.bind(this));
        } else {
            this.iterateQuests();
        }
    };
    this.onFileSelect = function($files) {
        if (! this.mission.id) {
            // We need an id to upload quest assets to S3
            this.mission.$save().then(function(mission) {
                S3Fcty.upload($files[0], 'missions', mission.id, 'uploads');
            });
        } else {
            S3Fcty.upload($files[0], 'missions', this.mission.id, 'uploads');
        }
    };
    this.deleteMission = function() {this.mission.$delete()};
}

/* === Controller Declarations === */
angular.module('planetApp')
    .controller('MissionCtrl', MissionCtrl)
    .controller('MissionFormCtrl', MissionFormCtrl);
