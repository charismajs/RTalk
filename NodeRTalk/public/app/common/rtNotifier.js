/**
 * Created by LuckyJS on 2014. 8. 28..
 */
angular.module('app').value('rtToastr', toastr);

angular.module('app').factory('rtNotifier', function (rtToastr) {
  return {
    notify: function (msg) {
      rtToastr.success(msg);
      console.log(msg);
    }
  }
});