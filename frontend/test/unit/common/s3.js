'use strict';

describe('resource factories', function() {

    beforeEach(module('planetApp'));

    it('check the existence of S3 service',
        inject(function(S3) {
            expect(S3).toBeDefined();
    }));
});
