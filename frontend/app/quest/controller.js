var questCtrlUtil = {
    upload: function($files, quest, S3) {
        S3.upload($files[0], 'quests', quest.id, 'uploads').then(
            function(iconUrl) {
                quest.icon_url = iconUrl;
        });
    }
};

planetApp.controller('QuestCtrl', [
    '$scope', '$stateParams', 'ResourceFactory', 'S3', 
    function($scope, $stateParams, ResourceFactory, S3 ) {
        this.quest = ResourceFactory('quests').get({id: $stateParams.id})
        // have to wrap $scope.quest.$put in a new function as the promise
        // won't be back in time to do a $scope.save = $scope.quest.$put
        this.save = function() {this.quest.$put()};
        this.onFileSelect = function($files) {
            questCtrlUtil.upload($files, this.quest, S3);
        };
        this.deleteQuest = function() {this.quest.$delete()};
}]);

planetApp.controller('QuestFormCtrl', [
    '$scope', 'ResourceFactory', 'S3', '$stateParams', '$state',
    function($scope, ResourceFactory, S3, $stateParams, $state) {
        if ($state.is('quests.form')) {
            $state.go('quests.form.basic');
        }
        if ($stateParams.id) {
            this.quest = ResourceFactory('quests').get({id: $stateParams.id});
        } else {
            this.quest = new (ResourceFactory('quests'));
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
                    questCtrlUtil.upload($files, quest, S3);
                });
            } else {
                questCtrlUtil.upload($files, this.quest, S3);
            }
        };
}]);
