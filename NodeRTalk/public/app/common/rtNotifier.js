/**
 * Created by LuckyJS on 2014. 8. 28..
 */
angular.module('app').value('rtToastr', toastr);

angular.module('app').factory('rtNotifier', function (rtToastr) {
  rtToastr.options.timeout = 30;
  rtToastr.options.extendedTimeOut = 60;

  return {
    info: function (msg) {
      rtToastr.info(msg);
      console.log(msg);
    },

    success: function(msg) {
      rtToastr.success(msg);
      console.log(msg);
    },

    error: function(msg) {
      rtToastr.error(msg);
      console.log(msg);
    },

    warning: function(msg) {
      rtToastr.warning(msg);
      console.log(msg);
    }
  }
});