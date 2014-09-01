/**
 * Created by LuckyJS on 2014. 8. 29..
 */
angular.module('app').factory('rtWriteContents', function($resource) {
  console.log('inWriteContents');

  var resource = $resource('/write', {
//    create: {method: 'POST', isArray: false}
  });

  return resource;
});

