from django.core.exceptions import ValidationError
# from django.core.validators import RegexValidator
from django.utils import dateparse, timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

import re


@deconstructible
class IDNumberValidator:
    """
    验证中国大陆身份证号格式
    """
    regex = re.compile(
        r"(([1][1-5])|([2][1-3])|([3][1-7])|([4][1-6])|([5][0-4])|([6][1-5])|([7][1])|([8][1-2]))\d{4}"
        r"(([1][9]\d{2})|([2]\d{3}))(([0][1-9])|([1][0-2]))(([0][1-9])|([1-2][0-9])|([3][0-1]))"
        r"\d{3}[0-9xX]"
    )
    error_messages = {
        "format_error": _("请确保值为身份证号"),
        "birthday_error": _("请使用正确的出生日期"),
        "invalid": _("错误的身份证号"),
    }

    def __init__(self):
        pass

    def __call__(self, value):
        # 格式校验
        regex_matches = self.regex.fullmatch(str(value))
        if not regex_matches:
            raise ValidationError(
                self.error_messages["format_error"], 
                code = "format_error"
            )
        # 出生日期校验
        ck_error = self.check_birthday(value)
        if ck_error is not None:
            raise ck_error
        # 合法性校验
        ck_error = self.check_validation_code(value)
        if ck_error is not None:
            raise ck_error

    def __eq__(self, other):
        return (
            isinstance(other, IDNumberValidator) and
            self.regex == other.regex and
            self.error_messages == other.error_messages
        )

    def check_birthday(self, value):
        year, month, day = value[6:10], value[10:12], value[12:14]
        now_date = timezone.localdate()
        try:
            birthday = dateparse.parse_date("{}-{}-{}".format(year, month, day))
        except ValueError:
            return ValidationError(
                self.error_messages["birthday_error"],
                code = "birthday_error"
            )
        if birthday > now_date:
            return ValidationError(
                self.error_messages["birthday_error"],
                code = "birthday_error"
            )

    def check_validation_code(self, value):
        # 系数
        coeficients = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
        # 校验码
        validation_codes = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
        # 计算校验码
        vc_sum = 0
        for i in range(17):
            vc_sum += int(value[i]) * coeficients[i]
        target = validation_codes[vc_sum % 11].upper()
        current = value[17].upper()
        if current != target:
            return ValidationError(
                self.error_messages["invalid"],
                code = "invalid"
            )


@deconstructible
class PhoneNumberValidator:
    """
    验证中国大陆手机号
    """
    regex = re.compile(r"^1(3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8}$")
    error_messages = {
        "invalid": _("请使用正确的手机号码"),
    }
    
    def __init__(self):
        pass

    def __call__(self, value):
        regex_matches = self.regex.fullmatch(str(value))
        if not regex_matches:
            raise ValidationError(
                self.error_messages["invalid"], 
                code = "invalid"
            )

    def __eq__(self, other):
        return (
            isinstance(other, PhoneNumberValidator) and
            self.regex == other.regex and
            self.error_messages == other.error_messages
        )
