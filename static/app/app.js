var app = angular.module('fitnessApp', [
	'ngRoute',
	'ordinal',
	'angular-loading-bar',
	'ngAnimate',
	'oitozero.ngSweetAlert',

	'fitnessApp.home',
	'fitnessApp.week',
	'fitnessApp.athlete',
	'fitnessApp.navigation',

	'fitnessApp.weekService',
	'fitnessApp.athleteService',
	'fitnessApp.categoriesService',

	'fitnessApp.categorySelectorDirective',
	'fitnessApp.htmlService'
])
.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
	cfpLoadingBarProvider.includeSpinner = false;
}])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider.otherwise({ templateUrl: 'static/app/templates/404.html' });
}]);