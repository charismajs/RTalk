/**
 * Created by LuckyJS on 2014. 8. 28..
 */
angular.module('app').factory('rtContentsList', function($resource) {
  var resource = $resource('/list/:topN/:listN',  {topN:'@topN', listN:'@listN'}, {
    query: {method: 'GET', isArray: false}
  });

  return resource;
});
