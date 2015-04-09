'use strict';

angular.module('fitnessApp.athleteService', [])

.factory('srvAthlete', ['$http', function($http) {

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