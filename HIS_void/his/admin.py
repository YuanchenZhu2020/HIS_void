from django.contrib import admin

from .models import Department, Notice, Staff


class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "user", "name", "gender", "dept"
    )
    list_filter = ("gender", "dept")
    search_fields = ("name", "dept")
admin.site.register(Staff, StaffAdmin)

class DeptAdmin(admin.ModelAdmin):
    list_display = (
        "dept", "description"
    )
    list_filter = ("dept",)
    search_fields = ("dept",)
admin.site.register(Department, DeptAdmin)

class NoticeAdmin(admin.ModelAdmin):
    list_display = ("dept", "send_time",)
    list_filter = ("dept", "send_time",)
    search_fields = ("dept", "send_time", )
admin.site.register(Notice, NoticeAdmin)
