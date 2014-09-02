/**
 * Created by LuckyJS on 2014. 8. 29..
 */
angular.module('app').factory('rtWriteContents', function($resource) {
  var resource = $resource('/write', {
  });

  return resource;
});

