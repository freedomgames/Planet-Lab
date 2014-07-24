'use strict';

describe('quest controllers', function() {

  beforeEach(function(){
    this.addMatchers({
      toEqualData: function(expected) {
        return angular.equals(this.actual, expected);
      }
    });
  });

  beforeEach(module('planetApp'));

  describe('QuestCtrl', function(){
    var scope, ctrl, $httpBackend;

    beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
      $httpBackend = _$httpBackend_;
      $httpBackend.expectGET('/v1/quests/3').
          respond({name: 'snakes', summary: 'ladders'});

      scope = $rootScope.$new();
      ctrl = $controller('QuestCtrl', {$scope: scope, $stateParams: {id: 3}});
    }));

    it('should retrieve quests from the back end', function() {
      $httpBackend.flush();
      expect(scope.quest).toEqualData({name: 'snakes', summary: 'ladders'});
    });
  });
});
