from django.db import models
from django.utils.translation import gettext_lazy as _

from patient.models import PatientUser
from his.models import HospitalTitle, Staff
from pharmacy.models import MedicineInfo


class TitleRegisterNumber(models.Model):
    """
    职称-挂号数对应表
    """
    title = models.OneToOneField(
        HospitalTitle, 
        primary_key = True,
        on_delete = models.CASCADE,
        verbose_name = _("职称")
    )
    register_number = models.PositiveIntegerField(verbose_name = _("挂号数限额"))

    class Meta:
        verbose_name = _("职称-挂号数")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Title {} | RegNum {}>".format(self.title, self.register_number)


class RemainingRegistration(models.Model):
    """
    医生剩余挂号数
    """
    medical_staff = models.OneToOneField(
        Staff, 
        on_delete = models.CASCADE, 
        related_name = "remaining_registration_set",
        related_query_name = "remaining_registrations",
        verbose_name = _("剩余挂号数"),
    )
    register_date = models.DateField(
        verbose_name = _("挂号日期"),
    )
    remain_quantity = models.PositiveIntegerField(
        blank = True,
        verbose_name = _("当日剩余挂号数")
    )

    class Meta:
        verbose_name = _("医生剩余挂号数")
        verbose_name_plural = verbose_name
        unique_together = ["medical_staff", "register_date"]
    
    def __str__(self) -> str:
        return "<RemRegNum {} | {} | {}>".format(
            self.medical_staff, self.register_date, self.remain_quantity
        )


class RegistrationInfo(models.Model):
    """
    挂号信息
    """
    RCLASS_ITEMS = [
        (0, _("门诊")),
        (1, _("急诊")),
    ]

    patient = models.ForeignKey(
        PatientUser, 
        on_delete = models.CASCADE,
        related_name = "registration_set",
        related_query_name = "registrations",
        verbose_name = _("患者")
    )
    reg_id = models.PositiveIntegerField(
        verbose_name = _("患者挂号编号"),
        help_text = _("该患者此生挂的第n个号")
    )

    medical_staff = models.ForeignKey(
        Staff, 
        on_delete = models.CASCADE, 
        related_name = "registration_set",
        related_query_name = "registrations",
        verbose_name = _("医生"),
    )
    appointment_date = models.DateTimeField(
        auto_created = True,
        editable = False,
        verbose_name = _("预约时间"),
        help_text = _("通过网页预约挂号的时间"),
    )
    registration_date = models.DateTimeField(
        verbose_name = _("挂号时间"),
        help_text = _("预约就诊的时间"),
    )
    reg_class = models.IntegerField(
        choices = RCLASS_ITEMS, 
        default = 0, 
        verbose_name = _("就诊类别")
    )

    illness_date = models.DateField(blank = True, verbose_name = _("患病日期"))
    chief_complaint = models.TextField(
        max_length = 512, 
        blank = True, 
        verbose_name = _("患者主诉")
    )
    diagnosis_results = models.TextField(
        max_length = 512, 
        blank = True, 
        verbose_name = _("确诊结果")
    )

    class Meta:
        verbose_name = _("挂号信息")
        verbose_name_plural = verbose_name
        unique_together = ["patient", "reg_id"]

    def __str__(self) -> str:
        return "<Registration {}-{}>".format(self.patient.patient_id, self.reg_id)


class Prescription(models.Model):
    """
    患者处方文件
    """
    registration_info = models.ForeignKey(
        RegistrationInfo, 
        on_delete = models.CASCADE, 
        related_name = "prescription_set",
        related_query_name = "prescriptions",
        verbose_name = _("挂号信息"),
    )
    prescription_date = models.DateTimeField(
        auto_created = True,
        editable = False,
        verbose_name = _("开具时间"),
    )
    medicine_num = models.PositiveIntegerField(blank = True, verbose_name = _("药品种类数"))
    medical_advice = models.TextField(
        max_length = 400,
        null = True,
        blank = True,
        verbose_name = _("医嘱")
    )
    payment_status = models.BooleanField(default = False, verbose_name = _("缴费状态"))

    class Meta:
        verbose_name = _("患者处方")
        verbose_name_plural = verbose_name
        unique_together = ["registration_info", "prescription_date"]

    def __str__(self) -> str:
        return "<Prescription {}-{} | {}>".format(
            self.registration_info.patient,
            self.registration_info.reg_id,
            self.prescription_date
        )


class PrescriptionDetail(models.Model):
    """
    患者处方细节
    """
    prescription_info = models.ForeignKey(
        Prescription, 
        on_delete = models.CASCADE, 
        related_name = "prescription_detail_set",
        related_query_name = "prescription_details",
        verbose_name = _("处方"),
    )
    detail_id = models.PositiveIntegerField(unique = True, verbose_name = _("细节编号"))

    medicine_info = models.ForeignKey(
        MedicineInfo, 
        on_delete = models.CASCADE,
        related_name = "prescription_detail_set",
        related_query_name = "prescription_details",
        verbose_name = _("药品信息"),
    )
    medicine_quantity = models.PositiveIntegerField(verbose_name = _("药品数量"))

    class Meta:
        verbose_name = _("处方细节")
        verbose_name_plural = verbose_name
        unique_together = ["prescription_info", "detail_id"]

    def __str__(self) -> str:
        return "<Prescription Detail {} of {}>".format(self.detail_id, self.prescription_info)
