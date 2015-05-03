'use strict';

angular.module('fitnessApp.athlete', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
	$routeProvider.when('/athlete/:athlete_id', {
		templateUrl: 'static/app/templates/athlete.html',
		controller: 'AthleteController',
		resolve: {
			athleteResponse: ['$route', 'srvAthlete', function($route, srvAthlete) {
				var athlete_id = $route.current.params.athlete_id;
				var athleteFactory = new srvAthlete();
				return athleteFactory.find(athlete_id);
			}]
		}
	});
}])

.controller('AthleteController', ['$scope', '$http', '$log', '$sce', 'html', 'athleteResponse', function($scope, $http, $log, $sce, html, athleteResponse) {
	$scope.category = 'Overall';

	$scope.athlete = athleteResponse.data;

	$scope.$watch('category', function() {
		$scope.changeCategory();
	});

	$scope.changeCategory = function() {
		var url;

		$http.get('/api/athletes/' + $scope.athlete.usag_id + '/stats?category=' + $scope.category).then(function(data) {
			$scope.results = data.data;
		});

		$scope.graphUrl = '/api/athletes/' + $scope.athlete.usag_id + '/graph?category=' + $scope.category;
		$http.get($scope.graphUrl).then(function(data) {
			$scope.graph = data.data;
		}, function(error) {
			// Failure
			$scope.graph = '<div class="alert alert-danger"><strong><i class="fa fa-exclamation-circle"></i> Error</strong> There was a problem retrieving this graph</div>';
		});
	};

	$scope.renderHtml = html.render;

}]);
