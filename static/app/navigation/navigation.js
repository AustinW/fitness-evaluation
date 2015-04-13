'use strict';

angular.module('fitnessApp.navigation', [])

.controller('NavigationBarController', ['$scope', '$http', 'srvWeeks', 'srvAthlete', 'SweetAlert', function($scope, $http, srvWeeks, srvAthlete, SweetAlert) {
	var athleteFactory = new srvAthlete();

	athleteFactory.all().then(function() {
		$scope.athletes = athleteFactory.athletes;
	});

	var weeksFactory = new srvWeeks();

	weeksFactory.all().then(function() {
		$scope.weeks = weeksFactory.weeks;
	});

	$scope.clearCache = function() {
		$http.get('/api/clear-cache').then(function(response) {
			var message = response.data.message;

			SweetAlert.swal({
				title: 'Cleared',
				text: message,
				timer: 2000,
				type: 'success'
			});
		});
	}
}]);