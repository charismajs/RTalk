/**
 * Created by LuckyJS on 2014. 8. 28..
 */
angular.module('app').value('rtToastr', toastr);

angular.module('app').factory('rtNotifier', function (rtToastr) {
//  rtToastr.options.showDuration = 300;
//  rtToastr.options.hideDuration = 1000;
  rtToastr.options.timeout = 500;
  rtToastr.options.extendedTimeOut = 500;

  return {
    info: function (msg) {
//      rtToastr.info(msg);
      alert(msg);
      console.log(msg);
    },

    success: function(msg) {
//      rtToastr.success(msg);
      alert(msg);
      console.log(msg);
    },

    error: function(msg) {
//      rtToastr.error(msg);
      alert(msg);
      console.log(msg);
    },

    warning: function(msg) {
//      rtToastr.warning(msg);
      alert(msg);
      console.log(msg);
    }
  }
});