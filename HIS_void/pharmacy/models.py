from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class MedicineInfo(models.Model):
    """
    药品信息
    """
    SPECIAL_ITEMS = (
        (1, '麻醉药品'),
        (2, '精神药品'),
        (3, '毒性药品'),
        (4, '放射性药品'),
        (0, '普通药品'),
    )

    medicine_id   = models.CharField(
        max_length = 6,
        primary_key = True,
        unique = True,
        verbose_name = _("药品编号"),
        help_text = _("药品的全局编号"),
    )
    medicine_name = models.CharField(max_length = 100, verbose_name = _("药品名称"))
    content_spec  = models.CharField(max_length = 20, verbose_name = _("含量规格"))
    package_spec  = models.CharField(max_length = 20, verbose_name = _("包装规格"))
    cost_price    = models.FloatField(
        validators = [MinValueValidator(0),],
        verbose_name = _("成本价")
    )
    retail_price  = models.FloatField(
        validators = [MinValueValidator(0),],
        verbose_name = _("零售价")
    )
    stock_num = models.PositiveIntegerField(default = 0, verbose_name = _("库存数量"))
    shelf_day = models.PositiveIntegerField(
        verbose_name = _("保质期"),
        help_text = _("以天为单位的保质期。")
    )
    special   = models.IntegerField(
        choices = SPECIAL_ITEMS, 
        default = 0, 
        verbose_name = _("特殊药品")
    )
    OTC = models.BooleanField(default = False, verbose_name = _("是否处方药"))

    class Meta:
        verbose_name = _("药品信息")
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return "<Medicine {}-{}>".format(self.medicine_id, self.medicine_name)


class MedicinePurchase(models.Model):
    """
    药品采购记录
    """
    medicine_info = models.ForeignKey(
        MedicineInfo,
        on_delete = models.CASCADE,
        related_name = "medicine_purchase_set",
        related_query_name = "medicine_purchases",
        verbose_name = _("药品信息")
    )
    batch_num     = models.PositiveIntegerField(verbose_name = _("批次编号"))
    purchase_date = models.DateField(verbose_name = _("采购日期"))
    purchase_quantity = models.PositiveIntegerField(verbose_name = _("采购数量"))

    class Meta:
        verbose_name = _("药品采购记录")
        verbose_name_plural = verbose_name
        unique_together = ["medicine_info", "batch_num"]

    def __str__(self) -> str:
        return "<Medicine Purchase {} | batch-{}>".format(self.medicine_info, self.batch_num)
