from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rbac.models import URLPermission
from patient.validators import IDNumberValidator


def update_last_login(sender, user, **kwargs):
    """
    A signal receiver which updates the last_login date for
    the user logging in.
    """
    user.last_login = timezone.now()
    user.save(update_fields = ['last_login'])


class PatientURLPermission(URLPermission):
    
    class Meta:
        verbose_name = _("患者URL访问权限")
        verbose_name_plural = verbose_name
        ordering = ["codename", "url"]

    def __str__(self):
        return "<URL Perm {}-{}>".format(self.codename, self.url)


class PatientUserManager(BaseUserManager):
    pass


class PatientUser(AbstractBaseUser):
    """
    使用自增字段 patient_id 作为主键，含义为就诊号。
    患者的 ID Number 可以为：
        1. 中国大陆身份证号
        2. 港澳居民来往内地通行证
        3. 台湾居民来往大陆通行证
        4. 护照 （http://cs.mfa.gov.cn/zggmcg/hz/hzjj_660445/t1200748.shtml）
    这里仅支持 1.
    """
    SEX_ITEMS = [
        (0, _("男")),
        (1, _("女")),
    ]
    ID_TYPE_ITEMS = [
        (0, _("中国大陆身份证")),
        (1, _("港澳居民来往内地通行证")),
        (2, _("台湾居民来往大陆通行证")),
        (3, _("护照")),
    ]

    patient_id = models.AutoField(primary_key = True, verbose_name = _("就诊号"))
    id_type = models.IntegerField(
        choices = ID_TYPE_ITEMS, 
        default = 0, 
        verbose_name = _("证件类型")
    )
    id_number = models.CharField(
        max_length = 18, 
        validators = [IDNumberValidator()], 
        verbose_name = _("证件号")
    )
    name = models.CharField(max_length = 20, verbose_name = _("姓名"))
    gender = models.IntegerField(choices = SEX_ITEMS, default = 0, verbose_name = _("性别"))
    birthday = models.DateField(verbose_name = _("出生日期"))
    phone = models.CharField(
        max_length = 11, 
        null = True, 
        verbose_name = _("手机号码")
    )
    past_illness = models.TextField(verbose_name = _("既往史"))
    allegic_history = models.TextField(verbose_name = _("过敏史"))

    create_time = models.DateTimeField(
        auto_now_add = True, 
        editable = False, 
        verbose_name = _("创建时间"),
    )
    is_admin = models.BooleanField(
        default = False, 
        editable = False,
        verbose_name = _("管理员"),
        help_text = _("决定该用户是否能够访问 /admin 页面。"),
    )

    objects = PatientUserManager()

    USERNAME_FIELD = "patient_id"
    REQUIRED_FIELDS = ["id_number"]

    def get_patient_id(self) -> str:
        """
        将自增ID转换为 N 位数字定长字符串。N 在 settings 中由 PATIENT_ID_LEN 设置。
        """
        N = settings.PATIENT_ID_LEN
        pid = str(self.patient_id)
        # 验证 patient id 的长度是否超过设置的最大长度
        if len(pid) > N:
            raise ValidationError(
                "患者数量超过 patient_id 所设置的最大长度",
                "请在 sttings 中配置 patient_id 的长度。"
            )
        return pid.rjust(N, '0')

    class Meta:
        verbose_name = _("患者")
        verbose_name_plural = _('患者')
    
    def __str__(self):
        return "<Patient {}>".format(self.patient_id)

    @property
    def is_staff(self):
        """
        判断一个UserInfo是否是管理员账户，即是否能够访问 /admin 页面
        """
        return self.is_admin

    def is_authenticated(self):
        """
        如果是
        """
        return True

    def set_name(self, name):
        self.name = name
    
    def set_gender(self, gender):
        self.gender = gender
    
    def set_birthday(self, birthday):
        self.birthday = birthday

    def get_all_url_permissions(self):
        """
        返回 PatientUser 实例所具有的全部URL访问权限。
        """
        if self.is_anonymous:
            return set()

        # URL访问权限缓存字段名称
        urlperm_cache_name = "_urlperm_cache"
        if not hasattr(self, urlperm_cache_name):
            perms = PatientURLPermission.objects.all()
            perms = perms.values_list("codename", "url").order_by()
            # 设置URL访问权限缓存
            setattr(self, urlperm_cache_name, {"{}.{}".format(cn, url) for cn, url in perms})
        return getattr(self, urlperm_cache_name)
