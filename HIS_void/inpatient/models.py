from django.db import models
from django.utils.translation import gettext_lazy as _

from his.models import Staff, Department, InpatientArea
from patient.models import PatientUser
from outpatient.models import RegistrationInfo
from pharmacy.models import MedicineInfo


class NursingRecord(models.Model):
    """
    护理记录
    """
    medical_staff = models.ForeignKey(
        Staff, 
        on_delete = models.CASCADE, 
        related_name = "nursing_record_set",
        related_query_name = "nursing_records",
        verbose_name = _("责任护士"),
    )
    patient = models.ForeignKey(
        PatientUser, 
        on_delete = models.CASCADE, 
        related_name = "nursing_record_set",
        related_query_name = "nursing_records",
        verbose_name = _("患者"),
    )
    nursing_date = models.DateField(
        auto_created = True,
        editable = False,
        verbose_name = _("护理时间"),
    )
    systolic = models.PositiveIntegerField(null = True, blank = True, verbose_name = _("收缩压"))
    diastolic = models.PositiveIntegerField(null = True, blank = True, verbose_name = _("舒张压"))
    temperature = models.FloatField(null = True, blank = True, verbose_name = _("体温"))
    note = models.TextField(
        max_length = 200, 
        null = True,
        blank = True, 
        verbose_name = _("备注")
    )

    class Meta:
        verbose_name = _("护理记录")
        verbose_name_plural = verbose_name
        unique_together = ["medical_staff", "patient", "nursing_date"]
    
    def __str__(self) -> str:
        return "<Nursing Record {}-{}-{}>".format(
            self.medical_staff,
            self.patient,
            self.nursing_date
        )


class HospitalRegistration(models.Model):
    """
    入院登记信息文件

    一级护理：粉红色标记，表示重点护理，但不派专人守护。对绝大多数重危病人来说，这就算是高等级的护理。
    二级护理：蓝色标记，表示病情无危险性，适于病情稳定的重症恢复期病人，或年老体弱、生活不能完全自理、不宜多活动的病人。
    三级护理：普通护理，不作标记。对这个护理级别的轻病人，护士每3～4小时巡视1次。
    特别护理(特护)：大红色标记，凡病情危重或重大手术后的病人，随时可能发生意外，需要严密观察和加强照顾。特护的都是重危病人，但重危病人不一定都要特护。
    """

    CARE_LEVEL_ITEMS = (
        (1, '一级护理'),
        (2, '二级护理'),
        (3, '三级护理'),
        (4, '四级护理'),
    )

    registration_info = models.OneToOneField(
        RegistrationInfo, 
        primary_key = True,
        on_delete = models.CASCADE, 
        verbose_name = _("挂号信息"),
    )
    dept = models.ForeignKey(
        Department,
        on_delete = models.CASCADE,
        verbose_name = _("所属科室"),
    )
    area = models.ForeignKey(
        InpatientArea, 
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = _("所属病区"),
    )
    bed_id = models.PositiveIntegerField(verbose_name = _("床位号"))
    reg_date = models.DateField(
        auto_created = True,
        editable = False,
        verbose_name = _("入院日期"),
    )
    care_level = models.PositiveIntegerField(
        default = 3, 
        choices = CARE_LEVEL_ITEMS, 
        verbose_name = _("护理级别")
    )
    duration = models.PositiveIntegerField(null = True, verbose_name = _("住院天数"))
    kin_phone = models.CharField(max_length = 11, verbose_name = _("家属电话"))
    discharge_status = models.BooleanField(default = False, verbose_name = _("即将出院状态"))

    class Meta:
        verbose_name = _("入院登记信息")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<HospReg {}>".format(self.registration_info)


class OperationInfo(models.Model):
    """
    手术信息文件

    一级手术：手术过程简单、技术难度较低、风险度较小的各种手术。
    二级手术：手术过程不复杂、技术难度一般、风险度中等的各种手术。
    三级手术：手术过程较复杂、技术难度较大、风险度较大的各种手术。
    四级手术：手术过程复杂、技术难度大、风险度大的各种手术。
    """
    LEVEL_CHOICES = (
        (1, '一级手术'),
        (2, '二级手术'),
        (3, '三级手术'),
        (4, '四级手术'),
    )

    registration_info = models.ForeignKey(
        RegistrationInfo, 
        on_delete = models.CASCADE, 
        verbose_name = _("挂号信息"),
    )
    opration_id = models.PositiveIntegerField(
        verbose_name = _("手术编号"),
        help_text = _("局部编号：每个医生-患者之间进行的第几场手术"),
    )
    operation_level = models.PositiveIntegerField(
        default = 1,
        choices = LEVEL_CHOICES, 
        verbose_name = _("手术等级")
    )
    operation_date = models.DateField(
        auto_created = True,
        editable = False,
        verbose_name = _("手术日期"),
    )
    operation_name = models.CharField(max_length = 40, verbose_name = _("手术名称"))
    operation_result = models.CharField(
        max_length = 20, 
        blank = True,
        verbose_name = _("手术结果")
    )
    operation_duration = models.TimeField(
        null = True,
        blank = True,
        verbose_name = _("手术持续时间"),
    )
    operation_recover = models.CharField(
        blank = True, 
        max_length = 10,
        verbose_name = _("预后结果"),
    )
    payment_status = models.BooleanField(default = False, verbose_name = _("缴费状态"))

    class Meta:
        verbose_name = _("手术信息")
        verbose_name_plural = verbose_name
        unique_together = ["registration_info", "opration_id"]
    
    def __str__(self) -> str:
        return "<Operation {}-{}>".format(self.registration_info, self.opration_id)


class NarcoticInfo(models.Model):
    """
    麻醉信息反馈
    """
    operation_info = models.OneToOneField(
        OperationInfo, 
        primary_key = True,
        on_delete = models.CASCADE, 
        related_name = "narcotic_set",
        related_query_name = "narcotics",
        verbose_name = _("手术信息"),
    )
    medicin_info = models.ForeignKey(
        MedicineInfo, 
        null = True,
        on_delete = models.SET_NULL, 
        related_name = "narcotic_set",
        related_query_name = "narcotics",
        verbose_name = _("麻醉药品信息"),
    )
    medical_staff = models.ForeignKey(
        Staff, 
        null = True,
        on_delete = models.SET_NULL, 
        related_name = "narcotic_set",
        related_query_name = "narcotics",
        verbose_name = _("麻醉师"),
    )

    class Meta:
        verbose_name = _("麻醉信息")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Narcotic {}-{}>".format(self.operation_info, self.medical_staff)

