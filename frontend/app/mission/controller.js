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

planetApp.controller('NewMissionCtrl', [
    '$scope', 'ResourceFactory', 'S3', 'ManyToOneResourceFactory', 'ManyToManyResourceFactory', 'curr',
    function($scope, ResourceFactory, S3, ManyToOneResourceFactory, ManyToManyResourceFactory, curr) {
        this.user_quests = ManyToOneResourceFactory('quests', 'users').query({parentId:curr});
        this.quests = [""];
        this.mission = new (ResourceFactory('missions'));
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
        this.setId = function(id) {
            this.quests.push(id);
        }
        this.saveQuests = function () {
            if (! this.mission.id) {
                // We need an id to upload quest assets to S3
                var that = this;
                this.mission.$save().then(function(that) {
                    for (var i; i < that.quests.length; i++) {
                        this.missionLink = new (ManyToManyResourceFactory('quests', that.quests[i], 'missions', this.mission.id));
                        this.missionLink.$save(); 
                    }
                });
            } else {
                for (var i; i < this.quests.length; i++) {
                    this.missionLink = new (ManyToManyResourceFactory('quests', this.quests[i], 'missions', this.mission.id));
                    this.missionLink.$save(); 
                }
            }
        };
        this.onFileSelect = function($files) {
            if (! this.mission.id) {
                // We need an id to upload quest assets to S3
                this.mission.$save().then(function() {
                    missionCtrlUtil.upload($files, this.mission, S3);
                });
            } else {
                missionCtrlUtil.upload($files, this.mission, S3);
            }
        };
}]);
