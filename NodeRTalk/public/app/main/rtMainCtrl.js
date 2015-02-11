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
    $scope.$broadcast('more-maker');
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

  $scope.expandContent = function (i) {

    var realHeight = $('#content_'+i)[0].scrollHeight;
    var viewHeight = $('#content_'+i).height();

    var defaultHeight = 70;
    if(viewHeight > defaultHeight){
      $("#content_"+i).animate({height:defaultHeight});
      // document.getElementById('content_'+i).style.height = defaultHeight+"px";
    }else{
      $("#content_"+i).animate({height:realHeight});
      // document.getElementById('content_'+i).style.height = realHeight+"px";
    }
  };
  $scope.expandTop = function (i) {

    var realHeight = $('#top_'+i)[0].scrollHeight;
    var viewHeight = $('#top_'+i).height();

    var defaultHeight = 70;
    if(viewHeight > defaultHeight){
      $("#top_"+i).animate({height:defaultHeight});
      // document.getElementById('top_'+i).style.height = defaultHeight+"px";
    }else{
      $("#top_"+i).animate({height:realHeight});
      // document.getElementById('top_'+i).style.height = realHeight+"px";
    }
  };

})
.directive('heightAdjust', ['$timeout', function ($timeout) {
    return {
        link: function ($scope, element, attrs) {
            $scope.$on('more-maker', function () {
                // $timeout(function () { 

                //   var defaultContentHeight = 70;

                //   var topCnt = $scope.contentsList.topn.length;
                //   for(i=0; i<topCnt ; i++){
                //     var viewHeight = $('#top_'+i).height();
                //     if(viewHeight > defaultContentHeight){
                //       document.getElementById("top_more_"+i).style.display = "inline-block";
                //       $("#top_"+i).animate({height:defaultContentHeight});
                //       // document.getElementById('top_'+i).style.height = defaultContentHeight+"px";
                      
                //     }
                //   }

                //   var totalCnt = $scope.contentsList.list.length;
                //   for(i=0; i<totalCnt ; i++){
                //     var viewHeight = $('#content_'+i).height();
                //     if(viewHeight > defaultContentHeight){
                //       document.getElementById("content_more_"+i).style.display = "inline-block";
                //       $("#content_"+i).animate({height:defaultContentHeight});
                //       // document.getElementById('content_'+i).style.height = defaultContentHeight+"px";
                      
                //     }

                //   }
                // }, 2000, false);

            })
        }
    };
}]);
