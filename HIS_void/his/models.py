from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from rbac.models import UserInfo, UserGroup


class Department(models.Model):
    """
    医院科室和部门。其编号范围为 [1, Inf)
    """
    dept = models.OneToOneField(
        UserGroup, 
        on_delete = models.CASCADE, 
        verbose_name = _("科室部门"),
    )
    description = models.TextField(verbose_name = _("简介"))

    class Meta:
        verbose_name = _("科室部门")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Department {}>".format(self.dept)

# UserGroup 添加新对象后，Department 会自动添加该对象
@receiver(post_save, sender = UserGroup)
def create_usergroup_department(sender, instance, created, **kwargs):
    if created:
        Department.objects.create(dept = instance)
    else:
        # print(Department.objects.filter(dept__ug_id = instance.ug_id))
        Department.objects.filter(dept__ug_id = instance.ug_id).update(dept = instance)    


class Staff(models.Model):
    """ 医院职工 """
    SEX_ITEMS = [
        (0, _("男")),
        (1, _("女")),
        (2, _("未知")),
    ]
    
    # null: 数据库中可以为空
    # blank: 表单显示
    user    = models.OneToOneField(
        UserInfo, 
        on_delete = models.CASCADE, 
        null = True, 
        blank = True, 
        verbose_name = _("登录信息")
    )
    name    = models.CharField(max_length = 128, verbose_name = _("职工姓名"))
    gender  = models.IntegerField(choices = SEX_ITEMS, default = 2, verbose_name = _("性别"))
    id_num  = models.CharField(max_length = 18, verbose_name = _("身份证号"))
    dept    = models.ForeignKey(
        UserGroup, 
        null = True, 
        on_delete = models.SET_NULL, 
        verbose_name = _("科室部门")
    )

    class Meta:
        verbose_name = _("职工")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Staff {}>".format(self.name)

# UserInfo 添加新对象后，Staff 会自动添加该对象
@receiver(post_save, sender = UserInfo)
def create_userinfo_staff(sender, instance, created, **kwargs):
    if created:
        Staff.objects.create(user = instance)
    else:
        # print(Staff.objects.filter(user__username = instance.username))
        Staff.objects.filter(user__username = instance.username).update(user = instance)
