'use strict';

angular.module('fitnessApp.categorySelectorDirective', [])

.directive('categorySelector', function() {
	return {
		restrict: 'E',
		
		replace: true,
		
		transclude: true,
		
		scope: {
			week: '='
		},

		controller: ['$scope', 'srvCategories', function($scope, srvCategories) {
			srvCategories.retrieve($scope.week).then(function(response) {
				$scope.categories = response.data;
			});
		}],

		template: '<select class="form-control" ng-options="item for item in categories"><option value="">Overall</option></select>',
		
		link: function(scope, element, attrs) {}
	}
});