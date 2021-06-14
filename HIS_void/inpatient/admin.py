from django.contrib import admin

from .models import NursingRecord, HospitalRegistration, OperationInfo, NarcoticInfo


@admin.register(NursingRecord)
class NursingRecordAdmin(admin.ModelAdmin):
    list_display = (
        "medical_staff", "hospital_reg", "nursing_date",
        "systolic", "diastolic", "temperature",
    )
    list_filter = ("medical_staff", "nursing_date", )
    search_fields = ("medical_staff", "hospital_reg", "nursing_date", )


@admin.register(HospitalRegistration)
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


@admin.register(OperationInfo)
class OperationInfoAdmin(admin.ModelAdmin):
    list_display = (
        "registration_info", "operation_id", "operation_level",
        "operation_date", "operation_name", "operation_result",
        "operation_duration", "operation_recover", "payment_status",
    )
    list_filter = ("registration_info", "operation_id", "operation_level", )
    search_fields = (
        "registration_info", "operation_id", "operation_level",
        "payment_status",
    )


@admin.register(NarcoticInfo)
class NarcoticInfoAdmin(admin.ModelAdmin):
    list_display = (
        "operation_info", "medicine_info", "medical_staff",
    )
    list_filter = ("operation_info", "medicine_info", "medical_staff", )
    search_fields = (
        "operation_info", "medicine_info", "medical_staff",
    )
