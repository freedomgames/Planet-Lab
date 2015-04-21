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
    '$scope', 'ResourceFactory', 'S3',
    function($scope, ResourceFactory, S3) {
        this.missions = new (ResourceFactory('missions'));
        this.save = function() {
            if (this.missions.id) {
                this.missions.$put();
            } else {
                this.missions.$save();
            }
        };
        this.onFileSelect = function($files) {
            if (! this.missions.id) {
                // We need an id to upload quest assets to S3
                this.missions.$save().then(function() {
                    missionCtrlUtil.upload($files, this.missions, S3);
                });
            } else {
                missionCtrlUtil.upload($files, this.missions, S3);
            }
        };
}]);
