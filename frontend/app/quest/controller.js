var updateScope = function($scope, $upload, S3Factory) {
    // Set common functions required by views of both controllers
    $scope.updateArrayItem = function(name, $event, $index) {
        $scope.quest[name][$index] = $event.target.value;
    };
    $scope.deleteArrayItem = function(name, $index) {
        $scope.quest[name].splice($index, 1);
    };
    $scope.newArrayItem = function(name) {
        $scope.quest[name].push('');
    };

    var s3Upload = function(file, uploadData) {
        // Given the file to upload an an object containing the form
        // data needed to upload the file to S3, perform the upload.
        // Then set the quest's icon URL to the just-uploaded file.
        uploadData.form_data.file = file;
        $upload.upload(uploadData.form_data).then(
            function(response) {
                if (response.status === 201) {
                    $scope.quest.icon_url = uploadData.s3_url;
                    alert('Upload Suceeded');
                } else {
                    alert('Upload Failed');
                }
        });
    };
    var beginUpload = function($files) {
        // Request the form data required to upload the file to S3
        // from the backend and then perform the upload.
        for (var i=0; i < $files.length; i++) {
            var file = $files[i];
            url = S3Factory('quests').get({
                id: $scope.quest.id,
                fileName: file.name,
                uploadName: 'uploads',
                mime_type: file.type});
            url.$promise.then(function() {
                s3Upload(file, url);
            });
        }
    };
    $scope.onFileSelect = function($files) {
        // Handle file uploads by sending them to S3.
        if (! $scope.quest.id) {
            // In case we are working with a new, un-saved quest.
            // We need an id to upload quest assets to S3
            $scope.quest.$save().then(function() {
                beginUpload($files);
            });
        } else {
            beginUpload($files);
        }
    }
};

planet_app.controller('QuestCtrl', [
    '$scope', '$stateParams', '$upload', 'ResourceFactory', 'S3Factory',
    function($scope, $stateParams, $upload, ResourceFactory, S3Factory) {
        $scope.quest = ResourceFactory('quests').get({id: $stateParams.id})
        // have to wrap $scope.quest.$put in a new function as the promise
        // won't be back in time to do a $scope.save = $scope.quest.$put
        $scope.save = function() {$scope.quest.$put()};
        updateScope($scope, $upload, S3Factory);
}]);

planet_app.controller('NewQuestCtrl', [
    '$scope', '$upload', 'ResourceFactory', 'S3Factory',
    function($scope, $upload, ResourceFactory, S3Factory) {
        $scope.quest = new (ResourceFactory('quests'));
        $scope.save = function() {
            if ($scope.quest.id) {
                $scope.quest.$put();
            } else {
                $scope.quest.$save();
            }
        };
        updateScope($scope, $upload, S3Factory);
}]);
