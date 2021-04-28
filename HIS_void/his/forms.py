from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class StaffLoginFrom(forms.Form):
    username = forms.CharField(
        max_length = 6,
        widget = forms.widgets.TextInput(
            attrs = {
                "class": "form-control",
                "name": "username",
                "autofocus": True,
                "required": True,
            }
        )
    )
    password = forms.CharField(
        max_length = 20,
        widget = forms.widgets.PasswordInput(
            attrs = {
                "class": "form-control",
                "name": "password",
                "required": True,
            }
        )
    )
    remembered = forms.BooleanField(
        # 非必填字段，默认值为 False
        required = False,
        widget = forms.widgets.CheckboxInput(
            attrs = {
                "class": "custom-control-input",
                "id": "basic_checkbox_1",
            }
        )
    )

    error_messages = {
        "wrong_username_or_password": _("账号或密码错误！"),
        "inactive": _("账户还未激活。"),
        "username_hint": _("用户名为工号。"),
    }

    def __init__(self, request = None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        self._remembered = False
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        进行：
            1. 获取“保持登录”选项状态
            2. 用户名格式验证
            3. 用户验证（Authentication）
            4. 账户激活验证（is active）
        """
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # 1. 获取“保持登录”选项状态
        self._remembered = self.cleaned_data.get("remembered")
        # 2. 用户名格式验证
        if len(username) == 6 and username.isdigit():
            # 3. 用户验证
            self.user_cache = authenticate(
                self.request, 
                username = username, 
                password = password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            # 4. 账户激活验证
            else:
                self.confirm_login_allowed(self.user_cache)
        else:
            raise self.get_invalid_username_error()

    def confirm_login_allowed(self, user):
        """
        判断用户账户是否已经激活
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code = "inactive",
            )
    
    def get_user(self):
        """
        获取验证成功的用户对象
        """
        return self.user_cache

    @property
    def remembered(self):
        return self._remembered

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["wrong_username_or_password"],
            code = "wrong_username_or_password",
        )

    def get_invalid_username_error(self):
        return ValidationError(
            self.error_messages["username_hint"],
            code = "username_hint"
        )
