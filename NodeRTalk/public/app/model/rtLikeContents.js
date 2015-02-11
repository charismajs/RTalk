/**
 * Created by LuckyJS on 2014. 8. 29..
 */
angular.module('app').factory('rtLikeContents', function($resource) {
  var resource = $resource('/like/:key', {key:'@key'}, {
    like: {method: 'GET', isArrary: false}
  });

  return resource;
});