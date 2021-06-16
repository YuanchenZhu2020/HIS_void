function validate_kin_phone(obj) {
  // 清除数字以外的字符
  obj.value = obj.value.replace(/[^\d]/g, "");
  // let reg = /^1(3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8}$/g;
  // let validate = reg.test(obj.value);
  // console.log(validate);
  // if (!validate) {
  //     $("#kin-phone-error").css("display", none);
  // }
}


(function ($) {
  $('.spinner .btn:first-of-type').on('click', function () {
    $('.spinner input').val(parseFloat((parseFloat($('.spinner input').val()) + 0.1).toFixed(2)));
  });
  $('.spinner .btn:last-of-type').on('click', function () {
    $('.spinner input').val(parseFloat((parseFloat($('.spinner input').val()) - 0.1).toFixed(2)));
  });
})(jQuery);


function validate_float(obj) {
  obj.value = obj.value.replace(/[^\d.]/g, ""); //清除“数字”和“.”以外的字符
  obj.value = obj.value.replace(/^\./g, ""); //验证第一个字符是数字而不是.
  obj.value = obj.value.replace(/\.{2,}/g, "."); //只保留第一个. 清除多余的.
  obj.value = obj.value.replace(".", "$#$").replace(/\./g, "").replace("$#$", ".");
}
