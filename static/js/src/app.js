var app = angular.module('fitnessApp', ['ordinal', 'angular-loading-bar', 'ngAnimate']);

app.controller('WeekController', ['$scope', '$http', '$log', '$sce', 'categories', 'html', function($scope, $http, $log, $sce, categories, html) {
	$scope.category = 'Overall Ranking';

	var segments = window.location.pathname.split( '/' );
	$scope.weekId = segments[segments.length - 1];

	$scope.$watch('category', function() {
		$scope.changeCategory();
	});

	$scope.changeCategory = function() {
		var url;

		$http.get('/api/week/' + $scope.weekId + '?category=' + $scope.category).then(function(data) {
			$scope.results = data.data;
		});

		$http.get('/api/week/' + $scope.weekId + '/graph?category=' + $scope.category).then(function(data) {
			$scope.graph = data.data;
		});
	};

	$scope.renderHtml = html.render;
}]);

app.controller('AthleteController', ['$scope', '$http', '$log', '$sce', 'categories', 'html', function($scope, $http, $log, $sce, categories, html) {
	$scope.category = 'Overall';

	var segments = window.location.pathname.split( '/' );
	$scope.athleteId = segments[segments.length - 1];

	$scope.$watch('category', function() {
		$scope.changeCategory();
	});

	$scope.changeCategory = function() {
		var url;

		$http.get('/api/athlete/' + $scope.athleteId + '?category=' + $scope.category).then(function(data) {
			$scope.results = data.data;
		});

		$http.get('/api/athlete/' + $scope.athleteId + '/graph?category=' + $scope.category).then(function(data) {
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
			week: '@'
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

app.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('<<');
	$interpolateProvider.endSymbol('>>');
});