/**
 * Created by LuckyJS on 2014. 8. 27..
 */
angular.module('app', ['ngResource', 'ngRoute', 'timer']);

angular.module('app').config(function($routeProvider, $locationProvider, ngSanitize) {
  $locationProvider.html5Mode(true);
  $routeProvider
    .when('/', {
      templateUrl: '/partials/main/main',
      controller: 'rtMainCtrl'
    });
});

