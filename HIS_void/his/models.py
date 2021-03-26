from django.db import models

from rbac import models as rbac_models


class Department(models.Model):
    """ 医院部门 """
    name = models.CharField(max_length = 32, verbose_name = "部门名称")

    class Meta:
        verbose_name = "部门表"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Department {}>".format(self.name)

class Staff(models.Model):
    """ 医院职工 """
    SEX_ITEMS = [
        (0, "男"),
        (1, "女"),
    ]
    
    user_obj = models.OneToOneField(rbac_models.UserInfo, on_delete = models.CASCADE, null = True, blank = True, verbose_name = "登录信息")
    name     = models.CharField(max_length = 128, verbose_name = "职工姓名")
    gender   = models.IntegerField(choices = SEX_ITEMS, verbose_name = "性别")
    dept_id  = models.ForeignKey(Department, null = True, on_delete = models.SET_NULL)

    class Meta:
        verbose_name = "职工表"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Staff {}>".format(self.name)

class LoginLog(models.Model):
    """ 登录日志 """
    # 删除 staff 时级联删除它的所有登录日志
    user_id      = models.ForeignKey(Staff, on_delete = models.CASCADE)
    create_time = models.DateTimeField(auto_now_add = True, editable = False, verbose_name = "登录时间")
    ip_address   = models.CharField(max_length = 256, verbose_name = "登录IP")

    class Meta:
        verbose_name = "登录日志"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<User {} Login at {} {}>".format(self.user_id, self.created_time, self.ip_address)
