planet_app.factory('S3', [
    '$q', '$upload', 'S3ResourceFactory',
    function($q, $upload, S3ResourceFactory) {
        var s3Upload = function(file, uploadData, uploadUrlPromise) {
            // Given the file to upload and an object containing the form
            // data needed to POST the file to S3, perform the upload.
            uploadData.upload_args.file = file;
            $upload.upload(uploadData.upload_args).then(function(response) {
                if (response.status === 201) {
                    uploadUrlPromise.resolve(uploadData.s3_url);
                } else {
                    uploadUrlPromise.reject('upload failed');
                }
            });
        };
        var beginUpload = function(file, resourceName, resourceId, uploadName) {
            // Request the form data required to upload the file to S3
            // from the backend and then perform the upload.
            var uploadUrlPromise = $q.defer();
            S3ResourceFactory(resourceName).get({
                id: resourceId,
                fileName: file.name,
                uploadName: uploadName,
                mime_type: file.type
            }).$promise.then(function(uploadData) {
                s3Upload(file, uploadData, uploadUrlPromise);
            });
            return uploadUrlPromise.promise;
        };

        return {upload: beginUpload};
}]);
