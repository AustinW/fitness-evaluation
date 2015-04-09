'use strict';

angular.module('fitnessApp.categoriesService', [])

.factory('srvCategories', ['$http', function($http) {

	return {
		retrieve: function(week) {
			var url = '/api/categories';

			if (week) {
				url += '?week=' + week;
			}

			return $http.get(url);
		}
	}

}]);