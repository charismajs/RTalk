/**
 * Created by LuckyJS on 2014. 9. 5..
 */
angular.module('app').filter('ignoreChar', function(text) {
  return text.replace(/\b\f\n\r\t\v\0/g, '');
});