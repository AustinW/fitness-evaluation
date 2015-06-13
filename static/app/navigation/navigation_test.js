describe('NavigationController', function() {
	var scope, httpBackend, createController;

	beforeEach(inject(function($rootScope, $httpBackend, $controller) {
		httpBackend = $httpBackend;
		scope = $rootScope.$new();

		createController = function() {
			return $controller('NavigationController', {
				'$scope': scope
			});
		};
	}));

	afterEach(function() {
		httpBackend.verifyNoOutstandingExpectation();
		httpBackend.verifyNoOutstandingRequest();
	});

	it('should run the test to get the list of weeks from the server', function() {
		var controller = createController();

		httpBackend.expect('GET', '/api/weeks').respond([
			{
				id: "oah2tm6",
				title: "4/04/2015"
			},
			{
				id: "oulqdya",
				title: "3/14/2015"
			}
		]);

		scope.$apply(function() {
			scope.runTest();
		});

		expect(scope.parseOriginalUrlStatus).toEqual('calling');

		httpBackend.flush();
	})
})