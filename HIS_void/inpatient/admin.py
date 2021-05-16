from django.contrib import admin

from .models import NursingRecord, HospitalRegistration, OperationInfo, NarcoticInfo


class NursingRecordAdmin(admin.ModelAdmin):
    list_display = (
        "medical_staff", "patient", "nursing_date", 
        "systolic", "diastolic", "temperature",
    )
    list_filter = ("medical_staff", "patient", "nursing_date", )
    search_fields = ("medical_staff", "patient", "nursing_date", )

admin.site.register(NursingRecord, NursingRecordAdmin)


class HospitalRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "registration_info", "area", "bed_id", 
        "reg_date", "care_level", "duration", 
        "kin_phone", "discharge_status",
    )
    list_filter = ("registration_info", "area", "bed_id", )
    search_fields = (
        "registration_info", "bed_id", "reg_date", "care_level", 
        "discharge_status",
    )

admin.site.register(HospitalRegistration, HospitalRegistrationAdmin)


class OperationInfoAdmin(admin.ModelAdmin):
    list_display = (
        "registration_info", "opration_id", "operation_level", 
        "operation_date", "operation_name", "operation_result", 
        "operation_duration", "operation_recover", "payment_status",
    )
    list_filter = ("registration_info", "opration_id", "operation_level", )
    search_fields = (
        "registration_info", "opration_id", "operation_level", 
        "payment_status",
    )

admin.site.register(OperationInfo, OperationInfoAdmin)


class NarcoticInfoAdmin(admin.ModelAdmin):
    list_display = (
        "operation_info", "medicine_info", "medical_staff", 
    )
    list_filter = ("operation_info", "medicine_info", "medical_staff", )
    search_fields = (
        "operation_info", "medicine_info", "medical_staff", 
    )

admin.site.register(NarcoticInfo, NarcoticInfoAdmin)

