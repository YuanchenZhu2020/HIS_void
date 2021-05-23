from django.contrib import admin

from his.models import (
    Department, JobType, Notice, Staff, DutyRoster, HospitalTitle, InpatientArea
)


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ("job_id", "job_name",)
    list_filter = ("job_id", "job_name",)
    search_fields = ("job_id", "job_name",)


@admin.register(HospitalTitle)
class HospitalTitleAdmin(admin.ModelAdmin):
    list_display = ("title_id", "title_name",)
    list_filter = ("title_id", "title_name",)
    search_fields = ("title_id", "title_name",)


@admin.register(InpatientArea)
class InpatientAreaAdmin(admin.ModelAdmin):
    list_display = ("area_id", )
    list_filter = ("area_id", )
    search_fields = ("area_id", )


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "user", "name", "gender", "dept"
    )
    list_filter = ("gender", "dept")
    search_fields = ("name", "dept")


@admin.register(Department)
class DeptAdmin(admin.ModelAdmin):
    list_display = (
        "usergroup", "description"
    )
    search_fields = ("usergroup",)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("dept", "send_time",)
    list_filter = ("dept", "send_time", "target_dept")
    search_fields = ("dept", "send_time", "target_dept")


@admin.register(DutyRoster)
class DutyRosterAdmin(admin.ModelAdmin):
    list_display = ("medical_staff", "working_day", "duty_area")
    list_filter = ("medical_staff", "working_day",)
    search_fields = ("medical_staff", "working_day",)
