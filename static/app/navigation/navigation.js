'use strict';

angular.module('fitnessApp.navigation', [])

.controller('NavigationBarController', ['$scope', '$http', '$route', '$timeout', 'srvWeeks', 'srvAthlete', 'SweetAlert', function($scope, $http, $route, $timeout, srvWeeks, srvAthlete, SweetAlert) {
	var athleteFactory = new srvAthlete();

	athleteFactory.all().then(function() {
		$scope.athletes = athleteFactory.athletes;
	});

	var weeksFactory = new srvWeeks();

	weeksFactory.all().then(function() {
		$scope.weeks = weeksFactory.weeks;
	});

	$scope.clearCache = function() {

		SweetAlert.swal({
			title: 'Are you sure?',
			text: 'This will cause the site to temporarily run a bit slower to ensure it has the latest results. Don\'t worry, it is safe to do.',
			type: 'warning',
			showCancelButton: true,
			confirmButtonColor: '#DD6B55',
			confirmButtonText: 'Yes, clear it',
			closeOnConfirm: false
		}, function(confirmed) {

			if (confirmed) {
				$http.get('/api/clear-cache').then(function(response) {
					var message = response.data.message;

					SweetAlert.swal({
						title: 'Cleared',
						text: message,
						timer: 2000,
						type: 'success'
					});

					$timeout(function() {
						// Reload the route when the cache has been cleared
						$route.reload();
					}, 2000);
				});
			}
		});
	}
}]);