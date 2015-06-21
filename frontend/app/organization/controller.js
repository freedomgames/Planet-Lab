var organizationCtrlUtil = {
    upload: function($files, organization, S3) {
        S3.upload($files[0], 'organizations', organization.id, 'uploads');
    }
};

planetApp.controller('OrganizationCtrl', [
    '$scope', '$stateParams', 'ResourceFactory', 'S3', 
    function($scope, $stateParams, ResourceFactory, S3 ) {
        this.organization = ResourceFactory('organization').get({id: $stateParams.id})
}]);

planetApp.controller('NewOrganizationCtrl', [
    '$scope', 'ResourceFactory', 'S3',
    function($scope, ResourceFactory, S3) {
        this.organizations = new (ResourceFactory('organizations'));
        this.save = function() {
            if (this.organizations.id) {
                this.organizations.$put();
            } else {
                this.organizations.$save();
            }
        };
        this.onFileSelect = function($files) {
            if (! this.organizations.id) {
                // We need an id to upload quest assets to S3
                this.organizations.$save().then(function() {
                    organizationsCtrlUtil.upload($files, this.organizations, S3);
                });
            } else {
                organizationCtrlUtil.upload($files, this.organization, S3);
            }
        };
}]);
