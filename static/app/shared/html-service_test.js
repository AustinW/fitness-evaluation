'use strict';

var mock, html, $sce, $sceDelegate;

describe('fitnessApp.htmlService module', function() {

  beforeEach(function() {
    mock = {html: jasmine.createSpy()};

    module('fitnessApp.htmlService')

    inject(function($injector) {
      html = $injector.get('html');
      $sce = $injector.get('$sce');
      $sceDelegate = $injector.get('$sceDelegate');
    });
  });

  describe('html service', function(){

    it('should pass html data through as raw html', function() {

      

      // var content = '<strong>Test</strong>';
      // var rendered = html.render(content);

      // var verify = $sceDelegate.trustAs($sce.HTML, content);
      // console.log(verify.properties);

      // expect(verify).toEqual('<strong>Test</strong>');
      //spec body
      //var view1Ctrl = $controller('View1Ctrl');
      //expect(view1Ctrl).toBeDefined();

      // var users = ['jack', 'igor', 'jeff'];
      // var sorted = sortUsers(users);
      // expect(sorted).toEqual(['jeff', 'jack', 'igor']);

    });

  });
});