from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentRecord(models.Model):
    """
    缴费记录表，记录缴费项目信息
    """
    ITEM_TYPE_ITEMS = (
        (0, _("挂号")),
        (1, _("检查检验")),
        (2, _("手术")),
        (3, _("处方")),
        (4, _("出院结算")),
    )

    PAY_STATUS_ITEMS = (
        (0, _("未缴费")),
        (1, _("缴费成功")),
        (2, _("缴费失败")),
    )

    trade_no = models.CharField(
        primary_key = True, 
        max_length = 64, 
        verbose_name = _("订单号")
    )
    total_amount = models.FloatField(
        validators = [MinValueValidator(0),], 
        verbose_name = _("总订单费用")
    )
    timestamp = models.DateTimeField(
        auto_now_add = True,
        editable = False,
        verbose_name = _("订单时间"),
        help_text = _("HIS系统创建订单的时间。")
    )
    item_type = models.IntegerField(
        choices = ITEM_TYPE_ITEMS,
        verbose_name = _("项目类型"),
        help_text = _("不同项目类型对应着不同的表，例如检查检验表、手术信息表、处方表等。")
    )
    item_name = models.CharField(max_length = 64, verbose_name = _("项目名称"))
    item_pk = models.CharField(
        max_length = 64,
        verbose_name = _("记录主键"),
        help_text = _("以'-'连接的主键值。例如，该条缴费记录对应一个患者检查检验，需要主键 (reg_id, test_id) 来索引。")
    )
    is_pay = models.IntegerField(
        default = 0,
        choices = PAY_STATUS_ITEMS,
        verbose_name = _("缴费状态"),
        help_text = _("0代表未缴费，1代表成功缴费, 2代表缴费失败")
    )

    def __str__(self) -> str:
        return "<Payment {}>".format(self.trade_no)
    
    class Meta:
        verbose_name = _("缴费记录")
        verbose_name_plural = verbose_name
