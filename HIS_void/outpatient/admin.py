from django.contrib import admin

from outpatient.models import (
    RegistrationInfo, Prescription, PrescriptionDetail, 
    TitleRegisterNumber, RemainingRegistration
)


@admin.register(TitleRegisterNumber)
class TitleRegisterNumberAdmin(admin.ModelAdmin):
    list_display = ("title", "registration_number")
    list_filter = ("title", )
    search_fields = ("title", "registration_number")


@admin.register(RemainingRegistration)
class RemainingRegistrationAdmin(admin.ModelAdmin):
    list_display = ("medical_staff", "register_date", "remain_quantity", )
    list_filter = ("medical_staff", "register_date", )
    search_fields = ("medical_staff", "register_date", )


@admin.register(RegistrationInfo)
class RegistrationInfoAdmin(admin.ModelAdmin):
    list_display = (
        "patient", "reg_id", "medical_staff", "reg_class",
        "appointment_date", "registration_date",
    )
    list_filter = ("patient", "reg_id", "medical_staff", )
    search_fields = ("patient", "reg_id", "medical_staff", )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "registration_info", "prescription_date", "medicine_num",
        "medical_advice", "payment_status",
    )
    list_filter = ("registration_info", "prescription_date", "payment_status",)
    search_fields = ("registration_info", "prescription_date", "payment_status",)


@admin.register(PrescriptionDetail)
class PrescriptionDetailAdmin(admin.ModelAdmin):
    list_display = (
        "prescription_info", "detail_id", "medicine_info", "medicine_quantity",
    )
    list_filter = ("prescription_info", "detail_id", "medicine_info",)
    search_fields = ("prescription_info", "detail_id", "medicine_info",)
