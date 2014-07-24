'use strict';

describe('service', function() {

  // load modules
  beforeEach(module('planetApp'));

  // Test service availability
  it('check the existence of ResourceFactory factory',
      inject(function(ResourceFactory) {
          expect(ResourceFactory).toBeDefined();
    }));

  it('check the existence of S3ResourceFactory factory',
      inject(function(S3ResourceFactory) {
          expect(S3ResourceFactory).toBeDefined();
    }));

  it('check the existence of S3 service',
      inject(function(S3) {
          expect(S3).toBeDefined();
    }));
});
