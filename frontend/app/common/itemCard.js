/**
 * File: QuestMissionDrctv.js
 * Description: Directive to output a quest or mission tile
 * Dependencies: none
 * @ngInject
 *
 * @package Planet-Lab
 */

/* === Function Declaration === */
function itemCard () {
    return {
        restrict: 'A',
        require: '^ngModel',
        templateUrl: 'static/common/itemCard.html',
        scope: {
            ngModel: '=',
            questOrMission: '@'
        }
    }
}

/* === Factory Declaration === */
angular.module('planetApp')
    .directive('itemCard', itemCard);
