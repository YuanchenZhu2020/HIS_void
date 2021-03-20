from django.contrib import admin

from .models import Staff, Department, LoginLog


class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user_obj", "name", "gender", "dept_id"
    )
    list_filter = ("gender", "dept_id")
    search_fields = ("name", "dept_id")


class DeptAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name"
    )


class LoginLogAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user_id", "create_time", "ip_address"
    )
    list_filter = ("create_time", "ip_address")
    search_fields = ("create_time", "ip_address")


admin.site.register(Staff, StaffAdmin)
admin.site.register(Department, DeptAdmin)
admin.site.register(LoginLog, LoginLogAdmin)
