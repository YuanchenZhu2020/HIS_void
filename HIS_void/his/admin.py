from django.contrib import admin

from .models import Department, Staff, LoginLog


class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "user", "name", "gender", "dept"
    )
    list_filter = ("gender", "dept")
    search_fields = ("name", "dept")


class DeptAdmin(admin.ModelAdmin):
    list_display = (
        "dept", "description"
    )
    list_filter = ("dept",)
    search_fields = ("dept",)


class LoginLogAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user_id", "login_time", "ip_address"
    )
    list_filter = ("login_time", "ip_address")
    search_fields = ("login_time", "ip_address")


admin.site.register(Staff, StaffAdmin)
admin.site.register(Department, DeptAdmin)
admin.site.register(LoginLog, LoginLogAdmin)
