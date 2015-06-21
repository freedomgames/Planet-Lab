var missionCtrlUtil = {
    upload: function($files, mission, S3) {
        S3.upload($files[0], 'missions', mission.id, 'uploads');
    }
};

planetApp.controller('MissionCtrl', [
    '$scope', '$stateParams', 'ResourceFactory', 'S3', 
    function($scope, $stateParams, ResourceFactory, S3 ) {
        this.mission = ResourceFactory('missions').get({id: $stateParams.id})
}]);

planetApp.controller('MissionFormCtrl', [
    '$scope', 'ResourceFactory', 'S3', 'ManyToOneResourceFactory', '$stateParams', '$state', 'CurrentUser',
    function($scope, ResourceFactory, S3, ManyToOneResourceFactory, $stateParams, $state, CurrentUser) {
        if ($state.is('missions.form')) {
            $state.go('missions.form.basic');
        }
        
        CurrentUser.getCurrentUserId().then(function(id) {
            this.user_quests = ManyToOneResourceFactory('quests', 'users').query({parentId: id});
        });
        this.quests = [""];
        if ($stateParams.id) {
            this.mission = ResourceFactory('missions').get({id: $stateParams.id});
            console.log(this.mission)
        } else {
            this.mission = new (ResourceFactory('missions'));
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
                this.missionLink = new (ManyToOneResourceFactory('quests', 'missions'));
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
                    missionCtrlUtil.upload($files, mission, S3);
                });
            } else {
                missionCtrlUtil.upload($files, this.mission, S3);
            }
        };
        this.deleteMission = function() {this.mission.$delete()};
}]);
