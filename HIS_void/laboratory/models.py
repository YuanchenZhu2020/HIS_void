from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from his.models import Staff
from outpatient.models import RegistrationInfo


class TestItemType(models.Model):
    """
    检验项目类型
    TEST_TYPE_ITEMS = (
        (1, '临床'), 
        (2, '生物化学'),
        (3, '微生物'),
        (4, '寄生虫'),
        (5, '免疫'),
    )
    """
    inspect_type_id = models.BigAutoField(primary_key = True, verbose_name = _("检验项目类型编号"))
    inspect_type_name = models.CharField(max_length = 30, verbose_name = _("检验项目类型名称"))

    class Meta:
        verbose_name = _("检验项目类型")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Inspect Type {}-{}>".format(self.inspect_type_id, self.inspect_type_name)


class TestItem(models.Model):
    """
    检验项目
    """
    inspect_id = models.BigAutoField(primary_key = True, verbose_name = _("检验项目编号"))
    inspect_type = models.ForeignKey(
        TestItemType,
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = _("检验项目类型"),
    )
    inspect_name = models.CharField(max_length = 30, verbose_name = _("检验项目名称"))
    inspect_price = models.FloatField(
        validators = [MinValueValidator(0),],
        verbose_name = _("检验价格")
    )

    class Meta:
        verbose_name = _("检验项目")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Inspection {}-{}>".format(self.inspect_id, self.inspect_name)


class PatientTestItem(models.Model):
    """
    患者检验项目
    """
    registration_info = models.ForeignKey(
        RegistrationInfo, 
        on_delete = models.CASCADE, 
        related_name = "patient_test_item_set",
        related_query_name = "patient_test_items",
        verbose_name = _("挂号信息"),
    )
    test_id = models.PositiveIntegerField(
        verbose_name = _("检验序号"),
        help_text = _("A病人第X次挂号的第i项检验"),
    )
    test_item = models.ForeignKey(
        TestItem, 
        on_delete = models.CASCADE, 
        related_name = "patient_test_item_set",
        related_query_name = "patient_test_items",
        verbose_name = _("检验项目"),
    )
    handle_staff = models.ForeignKey(
        Staff, 
        on_delete = models.CASCADE, 
        related_name = "patient_test_item_set",
        related_query_name = "patient_test_items",
        verbose_name = _("责任人"),
    )
    issue_time = models.DateTimeField(
        auto_created = True,
        editable = False,
        verbose_name = _("开具时间"),
    )
    test_results = models.TextField(max_length = 400, blank = True, verbose_name = _("检验结果"))
    payment_status = models.BooleanField(default = False, verbose_name = _("缴费状态"))

    class Meta:
        verbose_name = _("患者检验项目")
        verbose_name_plural = verbose_name
        unique_together = ["registration_info", "test_id", "test_item"]
    
    def __str__(self) -> str:
        return "<Patient Test Item {}-{}-{}>".format(
            self.registration_info,
            self.test_id,
            self.test_item
        )


class EquipmentTypeInfo(models.Model):
    """
    设备类型信息
    """
    eq_type_id = models.BigAutoField(primary_key = True, verbose_name = _("设备类型编号"))
    eq_type_name = models.CharField(max_length = 100, verbose_name = _("设备类型名称"))

    class Meta:
        verbose_name = _("设备类型信息")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Equipment Type {}-{}>".format(self.eq_type_id, self.eq_type_name)


class EquipmentInfo(models.Model):
    """
    设备信息
    """
    equipment_id = models.BigAutoField(primary_key = True, verbose_name = _("设备全局编号"))
    equipment_type = models.ForeignKey(
        EquipmentTypeInfo, 
        null = True,
        on_delete = models.SET_NULL,
        related_name = "equipment_info_set",
        related_query_name = "equipment_infos",
        verbose_name = _("设备类型"),
    )
    equipment_model = models.CharField(max_length = 20, verbose_name = _("设备型号"))
    purchase_date = models.DateField(
        auto_created = True,
        editable = False,
        verbose_name = _("采购日期"),
    )
    start_using = models.DateField(verbose_name = _("启用日期"))
    lifetime = models.PositiveIntegerField(verbose_name = _("理论使用寿命"))

    class Meta:
        verbose_name = _("设备信息")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Equipment {}-{}>".format(self.equipment_id, self.equipment_model)
