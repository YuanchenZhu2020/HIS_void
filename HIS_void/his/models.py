from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from rbac import models as rbac_models


class Department(models.Model):
    """
    医院科室和部门。其编号范围为 [1, 30]
    """
    dept_id = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(30)], 
        verbose_name = _("科室部门编号")
    )
    name    = models.CharField(max_length = 32, verbose_name = _("科室部门名称"))

    class Meta:
        verbose_name = _("科室部门")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Department {}>".format(self.name)


class Staff(models.Model):
    """ 医院职工 """
    SEX_ITEMS = [
        (0, _("男")),
        (1, _("女")),
    ]
    
    # null: 数据库中可以为空
    # blank: 表单显示
    user    = models.OneToOneField(
        rbac_models.UserInfo, 
        on_delete = models.CASCADE, 
        null = True, 
        blank = True, 
        verbose_name = _("登录信息")
    )
    name    = models.CharField(max_length = 128, verbose_name = _("职工姓名"))
    gender  = models.IntegerField(choices = SEX_ITEMS, verbose_name = _("性别"))
    id_num  = models.CharField(max_length = 18, verbose_name = _("身份证号"))
    dept    = models.ForeignKey(
        Department, 
        null = True, 
        on_delete = models.SET_NULL, 
        verbose_name = _("科室部门")
    )

    class Meta:
        verbose_name = _("职工")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Staff {}>".format(self.name)


class LoginLog(models.Model):
    """
    登录日志
    """
    # 删除 staff 时级联删除它的所有登录日志
    user       = models.ForeignKey(
        Staff, 
        on_delete = models.CASCADE, 
        verbose_name = _("职工")
    )
    login_time = models.DateTimeField(
        auto_now_add = True, 
        editable = False, 
        verbose_name = _("登录时间")
    )
    ip_address = models.CharField(max_length = 256, verbose_name = _("登录IP"))

    class Meta:
        verbose_name = _("登录日志")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<User {} Login at {} {}>".format(self.user, self.login_time, self.ip_address)
