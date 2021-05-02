from django.contrib import admin

from .models import Department, Staff


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


admin.site.register(Staff, StaffAdmin)
admin.site.register(Department, DeptAdmin)
