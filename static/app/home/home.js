'use strict';

angular.module('fitnessApp.home', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
	$routeProvider.when('/', {
		templateUrl: 'static/app/templates/home.html',
		controller: 'HomeController'
	});
}])

.controller('HomeController', ['$scope', '$http', 'srvWeeks', function($scope, $http, srvWeeks) {
	var weeksFactory = new srvWeeks();

	weeksFactory.all().then(function() {
		$scope.weeks = weeksFactory.weeks;
	});
}]);