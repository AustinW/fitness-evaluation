'use strict';

angular.module('fitnessApp.navigation', [])

.controller('NavigationBarController', ['$scope', '$http', 'srvWeeks', 'srvAthlete', function($scope, $http, srvWeeks, srvAthlete) {
	var athleteFactory = new srvAthlete();

	athleteFactory.all().then(function() {
		$scope.athletes = athleteFactory.athletes;
	});

	var weeksFactory = new srvWeeks();

	weeksFactory.all().then(function() {
		$scope.weeks = weeksFactory.weeks;
	});
}]);