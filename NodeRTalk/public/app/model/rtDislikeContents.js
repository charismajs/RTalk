/**
 * Created by LuckyJS on 2014. 9. 25..
 */
angular.module('app').factory('rtDislikeContents', function($resource) {
  var resource = $resource('/dislike/:key', {key:'@key'}, {
    dislike: {method: 'GET', isArrary: false}
  });

  return resource;
});