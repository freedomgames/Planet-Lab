'use strict';


describe('CurrentUser service', function() {

    beforeEach(module('planetApp'));

    var $httpBackend;
    beforeEach(inject(function(_$httpBackend_) {
        $httpBackend = _$httpBackend_;
        $httpBackend.expectGET('/current-user').respond({'user_id': 7});
    }));

    it('should retrieve and cache the user id from the backend',
        inject(function(CurrentUser, $rootScope) {
            var retrieved = false;
            CurrentUser.getCurrentUserId().then(function(currentUserId) {
                retrieved = true;
                expect(currentUserId).toBe(7);
            });
            $httpBackend.flush();
            expect(retrieved).toBe(true);

            // Now we should be able to skip the $httpBackend.flush() call as
            // the result should be cached.
            var retrieved = false;
            CurrentUser.getCurrentUserId().then(function(currentUserId) {
                retrieved = true;
                expect(currentUserId).toBe(7);
            });
            // we need a $digest() for the promise handler to be called
            $rootScope.$digest()
            expect(retrieved).toBe(true);
    }));
});
