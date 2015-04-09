'use strict';

angular.module('fitnessApp.weekService', [])

.factory('srvWeeks', ['$http', function($http) {
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