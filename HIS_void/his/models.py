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
        return "<Department {} | UserGroup {}>".format(self.dept.name, self.dept.ug_id)

# UserGroup 添加新对象后，Department 会自动添加该对象
@receiver(post_save, sender = UserGroup)
def create_usergroup_department(sender, instance, created, **kwargs):
    if created:
        Department.objects.create(dept = instance)
    else:
        # print(Department.objects.filter(dept__ug_id = instance.ug_id))
        Department.objects.filter(dept__ug_id = instance.ug_id).update(dept = instance)    


class Notice(models.Model):
    """
    科室部门通知表
    """
    dept = models.ForeignKey(
        Department, 
        on_delete = models.CASCADE,
        related_name = 'not_dept',
        verbose_name = _("科室部门"),
    )
    send_time = models.DateTimeField(
        auto_now_add = True, 
        editable = False, 
        verbose_name = _("发送时间"),
    )
    content = models.TextField(
        null = True,
        blank = True, 
        verbose_name = _("通知正文")
    )

    class Meta:
        verbose_name = _("部门通知")
        verbose_name_plural = verbose_name
        unique_together = ["dept", "send_time"]

    def __str__(self) -> str:
        return "<通知 {} | {}>".format(self.dept.dept.name, self.send_time)


class HospitalTitle(models.Model):
    """
    医院职称
    """
    title_id = models.BigAutoField(primary_key = True, verbose_name = _("职称ID"))
    title_name = models.CharField(max_length = 20, verbose_name = _("职称名称"))

    class Meta:
        verbose_name = _("医院职称")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Title {}-{}>".format(self.title_id, self.title_name)


class JobType(models.Model):
    """
    工种
    """
    job_id = models.BigAutoField(primary_key = True, verbose_name = _("工种编号"))
    job_name = models.CharField(max_length = 20, verbose_name = _("工种名称"))

    class Meta:
        verbose_name = _("工种")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Job Type {}-{}>".format(self.job_id, self.job_name)


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
    title   = models.ForeignKey(
        HospitalTitle, 
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = _("职称"),
    )
    job     = models.ForeignKey(
        JobType,
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = _("工种"),
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

