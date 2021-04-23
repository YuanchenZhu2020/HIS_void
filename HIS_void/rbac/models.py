from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


# def _user_get_permissions(user, obj, from_name):
#     permissions = set()
#     name = 'get_%s_permissions' % from_name
#     for backend in auth.get_backends():
#         if hasattr(backend, name):
#             permissions.update(getattr(backend, name)(user, obj))
#     return permissions

def _user_has_perm(user, perm, obj = None):
    pass

class PermGroup(models.Model):
    title       = models.CharField(max_length = 32, verbose_name = "权限组名称")
    create_time = models.DateTimeField(auto_now_add = True, editable = False, verbose_name = "创建时间")
    # menu  = models.ForeignKey(Menu, blank = True, on_delete = models.CASCADE, verbose_name = "所属菜单")

    class Meta:
        verbose_name = "权限组"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<PermGroup {}>".format(self.title)


class Permission(models.Model):
    """ 权限信息 """
    title       = models.CharField(max_length = 32, unique = True, verbose_name = "权限名")
    url         = models.CharField(max_length = 128, unique = True, verbose_name = "URL")
    create_time = models.DateTimeField(auto_now_add = True, editable = False, verbose_name = "创建时间")
    # 一般为 list, add, del, edit
    perm_code   = models.CharField(max_length = 32, verbose_name = "权限代码")
    # 权限组
    perm_group  = models.ForeignKey(PermGroup, blank = True, on_delete = models.CASCADE, verbose_name = "所属权限组")
    # 内联外键，可包含多个本表内权限记录。为 NULL 时作为二级菜单使用
    pid         = models.ForeignKey(
        "Permission", null = True, blank = True, 
        on_delete = models.CASCADE, verbose_name = "所属二级菜单"
    )

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Permission {}>".format(self.title)


class Role(models.Model):
    """ 角色 """
    title       = models.CharField(max_length = 32, unique = True, verbose_name = "角色名")
    description = models.TextField(max_length = 300, default = "", verbose_name = "角色描述")
    create_time = models.DateTimeField(auto_now_add = True, editable = False, verbose_name = "创建时间")
    permissions = models.ManyToManyField(Permission, blank = True, verbose_name = "拥有权限")

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Role {}>".format(self.title)


class URLPermission(models.Model):
    name = models.CharField(
        max_length = 255, 
        unique = True, 
        verbose_name = _('权限名'),
        help_text = _("URL访问权限的名称。"),
    )
    url = models.CharField(
        max_length = 128, 
        unique = True, 
        verbose_name = _("URL"),
        help_text = _("用于匹配指定URL的正则表达式。"),
    )
    codename = models.CharField(
        max_length = 64, 
        verbose_name = _("权限代码"),
        help_text = _("简要概括URL访问权限作用的对象，建议使用英文单词和下划线。"),
    )
    create_time = models.DateTimeField(
        auto_now_add = True, 
        editable = False, 
        verbose_name = _("创建时间")
    )
    perm_group = models.ForeignKey(
        PermGroup, 
        null = True,
        blank = True, 
        on_delete = models.SET_NULL, 
        verbose_name = _("所属权限组"),
    )

    # objects = URLPermissionManager()

    class Meta:
        verbose_name = _("URL访问权限")
        verbose_name_plural = verbose_name
        ordering = ["codename", "url"]

    def __str__(self):
        return "<URL Perm {}-{}>".format(self.codename, self.url)

    # def natural_key(self):
    #     return (self.codename,) + self.content_type.natural_key()
    # natural_key.dependencies = ['contenttypes.contenttype']


class GroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name = name)


class UserGroup(models.Model):
    """
    用户组，是拥有相同特点的用户的集合。
    """
    ug_id = models.IntegerField(
        validators = [MinValueValidator(1)], 
        unique = True,
        verbose_name = _("用户组编号"),
        help_text = _("用户组编号，取值范围为 1 ~ Inf。"),
    )
    name  = models.CharField(
        max_length = 32, 
        unique = True,
        verbose_name = _("用户组名称"),
        help_text = _("科室、部门或项目组名称。"),
    )
    # URL访问权限
    url_permissions = models.ManyToManyField(
        URLPermission, 
        blank = True, 
        verbose_name = _("URL访问权限"),
        help_text = _("用户组具有的全部URL访问权限。")
    )

    objects = GroupManager()

    class Meta:
        verbose_name = _("用户组")
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<User Group {}-{}>".format(self.ug_id, self.name)

    def natural_key(self):
        return (self.name,)


class PermissionsMixin(models.Model):
    """
    用户具有的所有权限模型：
        - 超级用户
        - 用户组
        - URL访问权限
        - （行级资源权限）
    """
    # Perm Cond 1: 超级用户
    is_superuser = models.BooleanField(
        default = False, 
        verbose_name = _("超级用户"),
        help_text = _("超级用户具有全部权限。"),
    )
    # Perm Cond 2: 用户组
    groups = models.ManyToManyField(
        UserGroup,
        blank = True,
        related_name = "user_set",
        related_query_name = "user",
        verbose_name = _("用户组"),
        help_text = _("用户所属的用户组，用户能够获取所属用户组的全部权限。"),
    )
    # Perm Cond 3: URL访问权限
    url_permissions = models.ManyToManyField(
        URLPermission,
        blank = True,
        related_name = "urlperm_set",
        related_query_name = "urlperm",
        verbose_name = _("URL访问权限"),
        help_text = _("该用户具有的所有URL访问权限。"),
    )


class UserInfoManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        根据提供的用户名、密码以及其它字段创建用户
        """
        if not username:
            raise ValueError(_("必须设置用户名"))
        username = self.model.normalize_username(username)
        user     = self.model(username = username, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_user(self, username, password = None, **extra_fields):
        """
        创建用户，并设置为非管理员、非超级用户。
        """
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password = None, **extra_fields):
        """
        创建超级用户账号
        """
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_admin") is not True:
            raise ValueError(_("超级用户必须是管理员，请设置 is_admin=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("超级用户必须设置 is_superuser=True"))

        return self._create_user(username, password, **extra_fields)


class UserInfo(AbstractBaseUser, PermissionsMixin):
    # 以 6 位数字的工号作为登录账号
    # 患者账号单独管理
    # password    = models.CharField(max_length = 256, verbose_name = "登录密码")
    username = models.CharField(
        max_length = 6, 
        unique = True, 
        verbose_name = _("登录账号"),
        help_text = _("以 6 位数字的工号作为登录账户名。"),
    )
    create_time = models.DateTimeField(
        auto_now_add = True, 
        editable = False, 
        verbose_name = _("创建时间"),
    )

    is_active = models.BooleanField(
        default = True, 
        verbose_name = _("活动账户"),
        help_text = _("决定该用户是否为活动账户。"),
    )
    is_admin = models.BooleanField(
        default = False, 
        verbose_name = _("管理员"),
        help_text = _("决定该用户是否能够访问 /admin 页面。"),
    )

    objects = UserInfoManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return "<UsrInfo {}>".format(self.username)

    def has_perm(self, perm, obj = None):
        """
        判断用户是否拥有特定权限
        """
        # 已激活的超级用户拥有所有权限
        if self.is_active and self.is_superuser:
            return True
        return _user_has_perm(self, perm, obj)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """
        判断一个UserInfo是否是管理员账户，即是否能够访问 /admin 页面
        """
        return self.is_admin

    class Meta:
        verbose_name = _("用户")
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return "<User {}>".format(self.username)
