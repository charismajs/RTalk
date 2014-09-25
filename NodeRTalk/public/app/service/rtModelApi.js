/**
 * Created by LuckyJS on 2014. 8. 29..
 */
angular.module('app').service('rtModelApi', function(rtContentsList, rtWriteContents, rtLikeContents, rtDislikeContents) {
  var list = function(topN, listN, next) {
    console.log('-- start to get a list in list function');
    rtContentsList.query(
      {
        topN : topN,
        listN : listN
      }, function(result) {
        console.log('-- complete to get a list : ', result);
        next(result);
      }
    );
  };

  var write = function(message, next) {
    console.log('-- start to write a talk in write function');
    rtWriteContents.save(
      {
        talk: message
      }, function(result) {
        console.log('-- complete to write : ', result);
        next(result);
      }
    );
  };

  var like = function(contents, next) {
    console.log('-- start to like the talk in like function');
    rtLikeContents.like(
      {
        key: contents.k
      }, function(result) {
        console.log('-- complete to like : ', result);
        next(result);
      }
    );
  };

  var dislike = function(contents, next) {
    console.log('-- start to dislike the talk in like function');
    rtDislikeContents.dislike(
      {
        key: contents.k
      }, function(result) {
        console.log('-- complete to dislike : ', result);
        next(result);
      }
    );
  };

  return {
    list: list,
    write: write,
    like: like,
    dislike: dislike
  };
});