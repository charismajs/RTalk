/**
 * Created by LuckyJS on 2014. 8. 28..
 */
angular.module('app').controller('rtMainCtrl', function($scope, $interval, rtModelApi, rtNotifier) {
  var defaultTopN = '3', defaultListN = '0';
  $scope.contentsList = '';
  $scope.timeCount = 10;

  // get a contents List
  var getContentsList = function(topN, listN) {
//    console.log('topN in Angularjs : ', topN);
//    console.log('listN in Angularjs : ', listN);
    rtModelApi.list(topN || defaultTopN, listN || defaultListN, function(result) {
      $scope.contentsList = result;
    });
  };

  getContentsList();

//  $scope.getListOnTime = function() {
//    getContentsList();
//    $scope.timeCount = 10;
//  };

  // save a new contents
  $scope.saveContents = function() {
    rtModelApi.write($scope.msg, function(newContents) {
      getContentsList(topN, listN);
      $scope.msg = '';
      rtNotifier.notify('Saved it!!');
    });
  };

  // thumbs up
  $scope.likeContents = function(contents) {
    rtModelApi.like(contents, function(result) {
      getContentsList(topN, listN);
      rtNotifier.notify('Like it!!');
    });
  };

  $scope.getContentsList = getContentsList;
});