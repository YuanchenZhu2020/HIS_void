from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import PatientURLPermission, PatientUser
from externalapi.external_api import IDInfoQuery


class PatientUserCreationForm(forms.ModelForm):
    """
    Admin 中，患者创建新用户所需要的全部字段。包括密码重复输入字段。
    """
    password1 = forms.CharField(label = _("用户密码"), widget = forms.PasswordInput)
    password2 = forms.CharField(label = _("确认密码"), widget = forms.PasswordInput)
    phone = forms.CharField(
        max_length = 11,
        required = False,
        label = _("联系电话"),
        widget = forms.TextInput
    )

    class Meta:
        model = PatientUser
        fields = (
            "password", "name",
            "id_type", "id_number", "phone",
        )

    def clean_password2(self):
        # 检查前后输入的密码是否相同
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("前后输入的密码不匹配"))
        return password2

    def save(self, commit = True):
        """
        使用 hasher 处理第一次输入的密码并储存
        @commit: 是否提交到数据库
        """
        user = super().save(commit = False)
        user.set_password(self.cleaned_data["password1"])
        id_info_query = IDInfoQuery(user.id_number)
        user.set_name(id_info_query.get_name())
        user.set_gender(id_info_query.get_gender())
        user.set_birthday(id_info_query.get_birthday())
        if commit:
            user.save()
        return user


class PatientUserChangeForm(forms.ModelForm):
    """
    Admin 中，更新用户资料，包含用户模型的全部字段。密码显示哈希加密参数与部分密文
    """
    password = ReadOnlyPasswordHashField(label = _("用户密码哈希"))

    class Meta:
        model = PatientUser
        fields = (
            "password", "name",
            "id_type", "id_number", "phone",
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@admin.register(PatientUser)
class PatientUserAdmin(BaseUserAdmin):
    # form: 用户对象更改
    # add_form: 用户对象新增
    form = PatientUserChangeForm
    add_form = PatientUserCreationForm

    list_display = ("patient_id", "name", "create_time", "last_login")
    list_filter = ("patient_id", )
    fieldsets = (
        (None, {"fields": ("name", "id_type", "id_number", "phone")}),
    )
    # UserAdmin 使用方法 get_fieldsets，通过 add_fieldsets 定义创建对象时所用的字段。
    add_fieldsets = (
        (_("证件类型与编号"), {
            "classes": ("wide",),
            "fields": (
                "id_type", "id_number",
            ),
        }),
        (_("更改密码"), {
            "classes": ("wide",),
            "fields": (
                "password1", "password2",
            ),
        }),
        (_("个人信息"), {
            "classes": ("wide", ),
            "fields": ("phone", ),
        }),
    )
    search_fields = ("patient_id", "name", "id_type", "id_number")
    ordering = ("patient_id",)
    filter_horizontal = ()


@admin.register(PatientURLPermission)
class PatientURLPermissionAdmin(admin.ModelAdmin):
    list_display = (
        "codename", "url_regex", "create_time",
    )
    list_filter = ("create_time", )
    search_fields = ("codename", "url_regex")

