'use strict';

angular.module('fitnessApp.week', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
	$routeProvider.when('/week/:week_id', {
		templateUrl: 'static/app/templates/week.html',
		controller: 'WeekController',
		resolve: {
			weeksPromise: ['$route', 'srvWeeks', function($route, srvWeeks) {
				var week_id = $route.current.params.week_id;
				var weekFactory = new srvWeeks();
				return weekFactory.find(week_id);
			}]
		}
	});
}])

.controller('WeekController', ['$scope', '$http', '$routeParams', '$sce', 'html', 'weeksPromise', function($scope, $http, $routeParams, $sce, html, weeksPromise) {
	$scope.category = 'Overall Ranking';

	$scope.week = weeksPromise.data;

	$scope.$watch('category', function() {
		if ($scope.category == null) {
			$scope.category = 'Overall Ranking';
		}
		$scope.changeCategory();
	});

	$scope.changeCategory = function() {
		var url;

		if ($scope.week) {

			$http.get('/api/week/' + $scope.week.id + '?category=' + $scope.category).then(function(response) {
				$scope.results = response.data;
			});

			$http.get('/api/week/' + $scope.week.id + '/graph?category=' + $scope.category).then(function(response) {
				$scope.graph = response.data;
			});
		}
	};

	$scope.renderHtml = html.render;
}]);