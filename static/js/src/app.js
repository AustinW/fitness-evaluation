var app = angular.module('fitnessApp', ['ngRoute', 'ordinal', 'angular-loading-bar', 'ngAnimate']);

app.config(['$routeProvider', function($routeProvider) {
	$routeProvider
		.when('/', {
			templateUrl: 'static/templates/index.html',
			controller: 'IndexController'
		})
		.when('/week/:week_id', {
			templateUrl: 'static/templates/week.html',
			controller: 'WeekController',
			resolve: {
				weeksPromise: ['$route', 'srvWeeks', function($route, srvWeeks) {
					var week_id = $route.current.params.week_id;
					var weekFactory = new srvWeeks();
					return weekFactory.find(week_id);
				}]
			}
		})
		.when('/athlete/:athlete_id', {
			templateUrl: 'static/templates/athlete.html',
			controller: 'AthleteController',
			resolve: {
				athletePromise: ['$route', 'srvAthlete', function($route, srvAthlete) {
					var athlete_id = $route.current.params.athlete_id;
					var athleteFactory = new srvAthlete();
					return athleteFactory.find(athlete_id);
				}]
			}
		})
		.otherwise({ templateUrl: 'static/templates/404.html' });
}]);

app.controller('IndexController', ['$scope', '$http', 'srvWeeks', function($scope, $http, srvWeeks) {
	var weeksFactory = new srvWeeks();

	weeksFactory.all().then(function() {
		$scope.weeks = weeksFactory.weeks;
	});
}]);

app.controller('NavigationBarController', ['$scope', '$http', 'srvWeeks', 'srvAthlete', function($scope, $http, srvWeeks, srvAthlete) {
	var athleteFactory = new srvAthlete();

	athleteFactory.all().then(function() {
		$scope.athletes = athleteFactory.athletes;
	});

	var weeksFactory = new srvWeeks();

	weeksFactory.all().then(function() {
		$scope.weeks = weeksFactory.weeks;
	});
}]);

app.controller('WeekController', ['$scope', '$http', '$routeParams', '$sce', 'categories', 'html', 'weeks', 'weeksPromise', function($scope, $http, $routeParams, $sce, categories, html, weeks, weeksPromise) {
	$scope.category = 'Overall Ranking';

	$scope.week = weeksPromise.data;

	$scope.$watch('category', function() {
		$scope.changeCategory();
	});

	$scope.changeCategory = function() {
		var url;

		if ($scope.week) {

			$http.get('/api/week/' + $scope.week.id + '?category=' + $scope.category).then(function(data) {
				$scope.results = data.data;
			});

			$http.get('/api/week/' + $scope.week.id + '/graph?category=' + $scope.category).then(function(data) {
				$scope.graph = data.data;
			});
		}
	};

	$scope.renderHtml = html.render;
}]);

app.controller('AthleteController', ['$scope', '$http', '$log', '$sce', 'categories', 'html', 'athletePromise', function($scope, $http, $log, $sce, categories, html, athletePromise) {
	$scope.category = 'Overall';

	$scope.athlete = athletePromise.data;

	$scope.$watch('category', function() {
		$scope.changeCategory();
	});

	$scope.changeCategory = function() {
		var url;

		$http.get('/api/athletes/' + $scope.athlete.usag_id + '/stats?category=' + $scope.category).then(function(data) {
			$scope.results = data.data;
		});

		$http.get('/api/athletes/' + $scope.athlete.usag_id + '/graph?category=' + $scope.category).then(function(data) {
			$scope.graph = data.data;
		});
	};

	$scope.renderHtml = html.render;

}]);

app.directive('categorySelector', function() {
	return {
		restrict: 'E',
		replace: true,
		transclude: true,
		scope: {
			week: '='
		},
		controller: ['$scope', 'categories', function($scope, categories) {
			categories.retrieve($scope.week).then(function(data) {
				$scope.categories = data.data;
			});
		}],
		template: '<select class="form-control" ng-options="item for item in categories"><option value="">Overall</option></select>',
		link: function(scope, element, attrs) {}
	}
});

app.factory('srvWeeks', ['$http', function($http) {
	var WeekService = function() {
		this.week = null;
		this.weeks = null;
	};

	WeekService.prototype.all = function() {
		var self = this;

		return $http.get('/api/weeks').then(function(response) {
			self.weeks = response.data;
			return response;
		});
	};

	WeekService.prototype.find = function(week_id) {
		var self = this;

		return $http.get('/api/weeks/' + week_id).then(function(response) {
			self.week = response.data;
			return response;
		})
	};

	return WeekService;
}]);

app.factory('srvAthlete', ['$http', function($http) {

	var AthleteService = function() {
		this.athlete = null;
		this.athletes = null;
	};

	AthleteService.prototype.all = function() {
		var self = this;

		return $http.get('/api/athletes').then(function(response) {
			self.athletes = response.data;
			return response;
		});
	};

	AthleteService.prototype.find = function(usag_id) {
		var self = this;

		return $http.get('/api/athletes/' + usag_id).then(function(response) {
			self.athlete = response.data;
			return response;
		});
	};

	return AthleteService;
}]);

app.service('weeks', ['$http', function($http) {
	this.retrieve = function() {
		return $http.get('/api/weeks');
	};
}])

app.service('html', ['$sce', function($sce) {
	this.render = function(html) {
		return $sce.trustAsHtml(html);
	};
}]);

app.service('categories', ['$http', function($http) {
	this.retrieve = function(week) {
		var url = '/api/categories';
		if (week) {
			url += '?week=' + week;
		}

		return $http.get(url);
	};
}]);

app.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
	cfpLoadingBarProvider.includeSpinner = false;
}]);