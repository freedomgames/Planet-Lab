'use strict';

describe('resource factories', function() {

    beforeEach(module('planetApp'));

    it('check the existence of ResourceFactory factory',
        inject(function(ResourceFactory) {
            expect(ResourceFactory).toBeDefined();
    }));

    it('check the existence of S3ResourceFactory factory',
        inject(function(S3ResourceFactory) {
            expect(S3ResourceFactory).toBeDefined();
    }));
});
