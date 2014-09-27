/**
 * Created by LuckyJS on 2014. 8. 28..
 */
angular.module('app').controller('rtMainCtrl', function($scope, rtModelApi, rtNotifier) {
  var defaultTopN = '3', defaultListN = '0';
  $scope.contentsList = '';
  var updatePeriod = 20;

  // get a contents List
  var getContentsList = function(topN, listN) {
    rtModelApi.list(topN || defaultTopN, listN || defaultListN, function(result) {
      $scope.contentsList = result;
    });
  };

  var getListOnTime = function()
  {
    getContentsList();
    $scope.$broadcast('timer-set-countdown', updatePeriod);
    $scope.$broadcast('timer-start');
  };

  // save a new contents
  $scope.saveContents = function() {
    rtModelApi.write($scope.msg, function(result) {
      getListOnTime();
      $scope.msg = '';
      rtNotifier.success('Saved it!!');
    });
  };

  // thumbs up
  $scope.likeContents = function(contents) {
    rtModelApi.like(contents, function(result) {
      getListOnTime();
      rtNotifier.info('Like it!!');
    });
  };

  // thumbs down
  $scope.dislikeContents = function(contents) {
    rtModelApi.dislike(contents, function(result) {
      getListOnTime();
      rtNotifier.error('Dislike it!!');
    });
  };

  $scope.getContentsList = getContentsList;
  $scope.getListOnTime = getListOnTime;
});