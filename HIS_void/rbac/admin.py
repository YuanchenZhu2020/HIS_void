from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from .models import UserInfo, Role, Permission, PermGroup


# class UserInfoAdmin(admin.ModelAdmin):
#     list_display = (
#         "id", "username", "password1",
#     )
#     search_fields = ("username", )

class UserCreationForm(forms.ModelForm):
    """
    Admin 中，创建新用户所需要的全部字段。包括密码重复输入字段。
    """
    password1 = forms.CharField(label = _("用户密码"), widget = forms.PasswordInput)
    password2 = forms.CharField(label = _("确认密码"), widget = forms.PasswordInput)

    class Meta:
        model = UserInfo
        fields = ("username", "is_active", "is_admin", "is_superuser")

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
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Admin 中，更新用户资料，包含用户模型的全部字段。密码显示哈希加密参数与部分密文
    """
    password = ReadOnlyPasswordHashField(label = _("用户密码哈希"))

    class Meta:
        model = UserInfo
        fields = ("username", "password", "is_active")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # form: 用户对象更改
    # add_form: 用户对象新增
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("username", "is_admin", "create_time")
    list_filter = ("is_admin", "create_time")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("登录信息"), {"fields": ("last_login",)}),
        (_("个人信息"), {"fields": ()}),
        (_("人员权限"), {"fields": ("is_active", "is_admin", "is_superuser")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ("wide",),
            'fields': (
                "username", "password1", "password2", 
                "is_active", "is_admin", "is_superuser",
            ),
        }),
    )
    search_fields = ("username",)
    ordering = ("username",)
    filter_horizontal = ()

admin.site.register(UserInfo, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "description", "create_time"
    )
    list_filter = ("title", )
    search_fields = ("title", "create_time")


class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "url", "create_time", "perm_code", "perm_group", "pid"
    )
    list_filter = ("title", "perm_code")
    search_fields = ("create_time", "perm_code", "pid")


class PermGroupAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "create_time"
    )
    list_filter = ("title", )
    search_fields = ("title", "create_time")


# admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(PermGroup, PermGroupAdmin)
