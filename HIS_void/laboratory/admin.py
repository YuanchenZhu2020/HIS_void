from django.contrib import admin

from .models import TestItemType, TestItem, PatientTestItem


class TestItemTypeAdmin(admin.ModelAdmin):
    list_display = ("inspect_type_id", "inspect_type_name",)
    list_filter = ("inspect_type_id", "inspect_type_name",)
    search_fields = ("inspect_type_id", "inspect_type_name",)

admin.site.register(TestItemType, TestItemTypeAdmin)


class TestItemAdmin(admin.ModelAdmin):
    list_display = ("inspect_id", "inspect_type", "inspect_name", "inspect_price", )
    list_filter = ("inspect_id", "inspect_type", "inspect_name", )
    search_fields = ("inspect_id", "inspect_type", "inspect_name", )

admin.site.register(TestItem, TestItemAdmin)


class PatientTestItemAdmin(admin.ModelAdmin):
    list_display = (
        "registration_info", "test_id", "test_item", 
        "handle_staff", "issue_time", "payment_status", 
    )
    list_filter = (
        "registration_info", "test_id", "test_item", 
        "handle_staff", "payment_status", 
    )
    search_fields = (
        "registration_info", "test_id", "test_item", 
        "handle_staff", "payment_status", 
    )

admin.site.register(PatientTestItem, PatientTestItemAdmin)
