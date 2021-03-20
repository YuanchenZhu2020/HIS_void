from django.contrib import admin

from .models import UserInfo, Role, Permission, PermGroup


class UserInfoAdmin(admin.ModelAdmin):
    list_display = (
        "id", "username", "password", "create_time",
    )
    search_fields = ("username", "create_time")


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


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(PermGroup, PermGroupAdmin)
