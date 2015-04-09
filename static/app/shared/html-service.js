'use strict';

angular.module('fitnessApp.htmlService', [])

.service('html', ['$sce', function($sce) {
	this.render = function(html) {
		return $sce.trustAsHtml(html);
	};
}]);