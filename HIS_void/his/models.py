from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from rbac.models import UserInfo, UserGroup


class InpatientArea(models.Model):
    """
    病区

    INPATIENT_AREA_ITEMS = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]
    """
    area_id = models.CharField(max_length = 2, primary_key = True, verbose_name = _("病区"))

    class Meta:
        verbose_name = _("病区")
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return "<Inpatient Area {}>".format(self.area_id)


class DepartmentManager(models.Manager):
    use_in_migrations = True
    
    def get_by_dept_id(self, ug_id):
        try:
            dept = self.get(usergroup__ug_id = ug_id)
        except Department.DoesNotExist:
            dept = None
        return dept
    
    def get_by_dept_name(self, name):
        try:
            ug = self.get(usergroup__name = name)
        except Department.DoesNotExist:
            ug = None
        return ug

   
class Department(models.Model):
    """
    医院科室和部门。其编号范围为 [1, Inf)
    """
    ACCEPT_ITEMS = [
        (0, _("不接收患者")),
        (1, _("接收患者"))
    ]

    usergroup      = models.OneToOneField(
        UserGroup,
        primary_key = True,
        on_delete = models.CASCADE,
        verbose_name = _("科室部门"),
    )
    accept_patient = models.BooleanField(
        choices = ACCEPT_ITEMS,
        default = 0,
        verbose_name = _("接收患者"),
        help_text = _("是否向病人提供诊疗服务。")
    )
    description    = models.TextField(null = True, blank = True, verbose_name = _("简介"))

    objects = DepartmentManager()

    class Meta:
        verbose_name = _("科室部门")
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return "<Department {} | UserGroup {}>".format(self.usergroup.name, self.usergroup.ug_id)

    @property
    def name(self):
        return self.usergroup.name
    
    @property
    def dept_id(self):
        return self.usergroup.ug_id

# UserGroup 添加新对象后，Department 会自动添加该对象
@receiver(post_save, sender = UserGroup)
def create_usergroup_department(sender, instance, created, **kwargs):
    if created:
        Department.objects.create(dept = instance)
    else:
        # print(Department.objects.filter(dept__ug_id = instance.ug_id))
        Department.objects.filter(usergroup__ug_id = instance.ug_id).update(usergroup = instance)


class DeptAreaBed(models.Model):
    """
    科室-病区-床位表
    """
    dept   = models.ForeignKey(
        Department,
        on_delete = models.CASCADE,
        related_name = "deptbeds_set",
        related_query_name = "deptbeds",
        verbose_name = _("科室"),
    )
    area   = models.ForeignKey(
        InpatientArea,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = "deptbeds_set",
        related_query_name = "deptbeds",
        verbose_name = _("病区"),
    )
    bed_id = models.PositiveIntegerField(
        validators = [MinValueValidator(1),],
        verbose_name = _("床位号"),
        help_text = _("指定病区的第 n 个病床。"),
    )

    class Meta:
        verbose_name = _("科室-病区-床位")
        verbose_name_plural = verbose_name
        unique_together = ["dept", "area", "bed_id"]
    
    def __str__(self) -> str:
        return "<Bed {}-{}-{}>".format(self.dept.dept.name, self.area.area_id, self.bed_id)


class Notice(models.Model):
    """
    科室部门通知表
    """
    dept        = models.ForeignKey(
        Department,
        on_delete = models.CASCADE,
        related_name = "notice_set_send",
        related_query_name = "notices_send",
        verbose_name = _("科室部门"),
    )
    send_time   = models.DateTimeField(
        auto_now_add = True,
        editable = False,
        verbose_name = _("发送时间"),
    )
    content     = models.TextField(
        null = True,
        blank = True,
        verbose_name = _("通知正文")
    )
    target_dept = models.ManyToManyField(
        Department,
        related_name = "notice_set_recv",
        related_query_name = "notices_recv",
        verbose_name = _("目标科室部门"),
    )

    class Meta:
        verbose_name = _("部门通知")
        verbose_name_plural = verbose_name
        unique_together = ["dept", "send_time"]

    def __str__(self) -> str:
        return "<Notice {} | {}>".format(self.dept.usergroup.name, self.send_time)


class HospitalTitleManager(models.Manager):
    use_in_migrations = True

    def get_by_title_id(self, title_id):
        try:
            ht = self.get(title_id = title_id)
        except HospitalTitle.DoesNotExist:
            ht = None
        return ht
    
    def get_by_title_name(self, title_name):
        try:
            ht = self.get(title_name = title_name)
        except HospitalTitle.DoesNotExist:
            ht = None
        return ht


class HospitalTitle(models.Model):
    """
    医院职称
    TITLE_CHOICES = (
        (1, '住院医师'),
        (2, '主治医师'),
        (3, '副主任医师'),
        (4, '主任医师'),
    )
    """
    title_id   = models.BigAutoField(primary_key = True, verbose_name = _("职称ID"))
    title_name = models.CharField(max_length = 20, verbose_name = _("职称名称"))

    objects = HospitalTitleManager()

    class Meta:
        verbose_name = _("医院职称")
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return "<Title {}-{}>".format(self.title_id, self.title_name)


class JobTypeManager(models.Manager):
    use_in_migrations = True

    def get_by_job_id(self, job_id):
        try:
            jt = self.get(job_id = job_id)
        except JobType.DoesNotExist:
            jt = None
        return jt
    
    def get_by_job_name(self, job_name):
        try:
            jt = self.get(job_name = job_name)
        except JobType.DoesNotExist:
            jt = None
        return jt


class JobType(models.Model):
    """
    工种

    JOB_CHOICES = (
        (1, '医生'),
        (2, '护士'),
        (3, '药房医生'),
        (4, '检验医生'),
        (5, '财务'),
        (6, '运维'),
    )
    """
    job_id   = models.BigAutoField(primary_key = True, verbose_name = _("工种编号"))
    job_name = models.CharField(max_length = 20, verbose_name = _("工种名称"))

    objects = JobTypeManager()

    class Meta:
        verbose_name = _("工种")
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return "<Job Type {}-{}>".format(self.job_id, self.job_name)


class StaffManager(models.Manager):
    use_in_migrations = True

    def get_by_user(self, username):
        try:
            sf = self.get(user__username = username)
        except UserGroup.DoesNotExist:
            sf = None
        return sf


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
        null = True,
        blank = True,
        on_delete = models.CASCADE,
        verbose_name = _("登录信息")
    )
    name    = models.CharField(max_length = 128, verbose_name = _("职工姓名"))
    gender  = models.IntegerField(choices = SEX_ITEMS, default = 2, verbose_name = _("性别"))
    id_num  = models.CharField(max_length = 18, verbose_name = _("身份证号"))
    dept    = models.ForeignKey(
        Department,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = "staff_set",
        related_query_name = "staffs",
        verbose_name = _("科室部门")
    )
    title   = models.ForeignKey(
        HospitalTitle,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = "staff_set",
        related_query_name = "staffs",
        verbose_name = _("职称"),
    )
    job     = models.ForeignKey(
        JobType,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = "staff_set",
        related_query_name = "staffs",
        verbose_name = _("工种"),
    )

    objects = StaffManager()

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


class DutyRoster(models.Model):
    """
    医务人员排班表
    """
    WEEKDAY_ITEMS = [
        (1, '星期一'),
        (2, '星期二'),
        (3, '星期三'),
        (4, '星期四'),
        (5, '星期五'),
        (6, '星期六'),
        (7, '星期日'),
    ]

    medical_staff = models.ForeignKey(
        Staff,
        on_delete = models.CASCADE,
        related_name = "duty_roster_set",
        related_query_name = "duty_rosters",
        verbose_name = _("医务人员"),
    )
    working_day = models.PositiveIntegerField(
        choices = WEEKDAY_ITEMS,
        verbose_name = _("工作日"),
    )
    duty_area = models.ForeignKey(
        InpatientArea,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = "duty_roster_set",
        related_query_name = "duty_rosters",
        verbose_name = _("负责病区"),
    )
    # is_outpatient = models.BooleanField(
    #     default = 0,
    #     verbose_name = _("是否在门诊值班"),
    #     help_text = _("0代表在住院部值班，1代表在门诊值班。")
    # )

    class Meta:
        verbose_name = _("医务人员排班表")
        verbose_name_plural = verbose_name
        unique_together = ["medical_staff", "working_day"]

    def __str__(self) -> str:
        return "<Duty Roster {} {}>".format(self.medical_staff, self.working_day)
