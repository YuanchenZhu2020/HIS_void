from django.contrib import admin

from laboratory.models import (
    TestItemType, TestItem, PatientTestItem, 
    EquipmentTypeInfo, EquipmentInfo,
)


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


class EquipmentTypeInfoAdmin(admin.ModelAdmin):
    list_display = ("eq_type_id", "eq_type_name",)
    list_filter = ("eq_type_id", "eq_type_name",)
    search_fields = ("eq_type_id", "eq_type_name",)

admin.site.register(EquipmentTypeInfo, EquipmentTypeInfoAdmin)


class EquipmentInfoAdmin(admin.ModelAdmin):
    list_display = (
        "equipment_id", "equipment_type", "equipment_model", 
        "purchase_date", "start_using", "lifetime",
    )
    list_filter = ("equipment_id", "equipment_type", "equipment_model", )
    search_fields = ("equipment_id", "equipment_type", "equipment_model", )

admin.site.register(EquipmentInfo, EquipmentInfoAdmin)
