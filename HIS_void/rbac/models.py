from django.db import models
from django.contrib.auth import get_backends
from django.contrib.auth.models import Permission, AbstractBaseUser, BaseUserManager
from django.core.exceptions import PermissionDenied
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


def _user_get_obj_permissions(user, from_name):
    permissions = set()
    name = "get_{}_obj_permissions".format(from_name)
    for backend in get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user))
    return permissions

def _user_has_objperm(user, objperm):
    for backend in get_backends():
        if not hasattr(backend, "has_objperm"):
            continue
        try:
            if backend.has_objperm(user, objperm):
                return True
        except PermissionDenied:
            return False
    return False

def _user_has_module_objperms(user, app_label):
    for backend in get_backends():
        if not hasattr(backend, "has_module_objperms"):
            continue
        try:
            if backend.has_module_objperms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False


def _user_get_url_permissions(user, from_name):
    permissions = set()
    name = "get_{}_url_permissions".format(from_name)
    for backend in get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user))
    return permissions

def _user_has_urlperm(user, perm):
    for backend in get_backends():
        if not hasattr(backend, 'has_urlperm'):
            continue
        try:
            if backend.has_urlperm(user, perm):
                return True
        except PermissionDenied:
            return False
    return False

def _user_has_module_urlperms(user, url_regex):
    for backend in get_backends():
        if not hasattr(backend, "has_module_urlperms"):
            continue
        try:
            if backend.has_module_urlperms(user, url_regex):
                return True
        except PermissionDenied:
            return False
    return False


class ObjectPermission(models.Model):
    name = models.CharField(max_length = 255, verbose_name = _("对象权限名称"))
    permission = models.ForeignKey(
        Permission, 
        on_delete = models.CASCADE, 
        verbose_name = _("权限")
    )
    object_id = models.CharField(max_length = 255, verbose_name = _("对象ID"))
    create_time = models.DateTimeField(
        auto_now_add = True, 
        editable = False, 
        verbose_name = "创建时间"
    )

    class Meta:
        verbose_name = _("对象权限")
        verbose_name_plural = verbose_name
        unique_together = [["permission", "object_id"]]
        ordering = [
            "permission__content_type__app_label", 
            "permission__content_type__model", 
            "object_id"
        ]

    def __str__(self):
        return "<{} | {}>".format(self.permission, self.object_id)


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

    class Meta:
        verbose_name = _("URL访问权限")
        verbose_name_plural = verbose_name
        ordering = ["codename", "url"]

    def __str__(self):
        return "<URL Perm {}-{}>".format(self.codename, self.url)


class Role(models.Model):
    """ 角色 """
    title       = models.CharField(max_length = 32, unique = True, verbose_name = "角色名")
    description = models.TextField(max_length = 300, default = "", verbose_name = "角色描述")
    create_time = models.DateTimeField(
        auto_now_add = True, 
        editable = False, 
        verbose_name = "创建时间"
    )
    # URL访问权限
    url_permissions = models.ManyToManyField(
        URLPermission, 
        blank = True, 
        related_name = "role_set",
        related_query_name = "role",
        verbose_name = _("URL访问权限"),
        help_text = _("该角色拥有的URL访问权限"),
    )
    # 行级资源权限
    obj_permissions = models.ManyToManyField(
        ObjectPermission,
        blank = True, 
        related_name = "role_set",
        related_query_name = "role",
        verbose_name = _("对象资源权限"),
        help_text = _("该角色拥有的对象资源权限"),
    )

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Role {}>".format(self.title)


class GroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, ug_id, name):
        return self.get(ug_id = ug_id, name = name)
    
    def get_by_usergroup_id(self, ug_id):
        try:
            ug = self.get(ug_id = ug_id)
        except UserGroup.DoesNotExist:
            ug = None
        return ug
    
    def get_by_usergroup_name(self, name):
        try:
            ug = self.get(name = name)
        except UserGroup.DoesNotExist:
            ug = None
        return ug


class UserGroup(models.Model):
    """
    用户组，是拥有相同特点的用户的集合。具有三个权限模型：
        - 角色
        - URL访问权限
        - （行级资源权限）
    """
    ug_id = models.BigAutoField(
        primary_key = True,
        verbose_name = _("用户组编号"),
        help_text = _("用户组编号，取值范围为 1 ~ Inf。"),
    )
    name  = models.CharField(
        max_length = 32, 
        unique = True,
        verbose_name = _("用户组名称"),
        help_text = _("科室、部门或项目组名称。"),
    )
    create_time = models.DateTimeField(
        auto_now_add = True, 
        editable = False, 
        verbose_name = "创建时间"
    )
    # Perm Cond 1: 角色
    roles = models.ManyToManyField(
        Role,
        blank = True,
        related_name = "usergroup_set",
        related_query_name = "usergroup",
        verbose_name = _("角色"),
        help_text = _("用户组所拥有的角色，用户组能够获取所拥有角色的全部权限。"),
    )
    # Perm Cond 2: URL访问权限
    url_permissions = models.ManyToManyField(
        URLPermission, 
        blank = True, 
        related_name = "usergroup_set",
        related_query_name = "usergroup",
        verbose_name = _("URL访问权限"),
        help_text = _("用户组具有的全部URL访问权限。")
    )
    # Perm Cond 3: 行级资源权限
    obj_permissions = models.ManyToManyField(
        ObjectPermission,
        blank = True, 
        related_name = "usergroup_set",
        related_query_name = "usergroup",
        verbose_name = _("对象资源权限"),
        help_text = _("该用户组拥有的对象资源权限"),
    )

    objects = GroupManager()

    class Meta:
        verbose_name = _("用户组")
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<User Group {}-{}>".format(self.ug_id, self.name)

    def natural_key(self):
        return (self.ug_id, self.name,)


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
    # Perm Cond 3: 角色
    roles = models.ManyToManyField(
        Role,
        blank = True,
        related_name = "user_set",
        related_query_name = "user",
        verbose_name = _("角色"),
        help_text = _("用户所拥有的角色，用户能够获取所拥有角色的全部权限。"),
    )
    # Perm Cond 4: URL访问权限
    url_permissions = models.ManyToManyField(
        URLPermission,
        blank = True,
        related_name = "user_set",
        related_query_name = "user",
        verbose_name = _("URL访问权限"),
        help_text = _("该用户具有的所有URL访问权限。"),
    )
    # Perm Cond 5: 行级资源权限
    obj_permissions = models.ManyToManyField(
        ObjectPermission,
        blank = True, 
        related_name = "user_set",
        related_query_name = "user",
        verbose_name = _("对象资源权限"),
        help_text = _("该用户拥有的对象资源权限"),
    )

    # 获取URL访问权限
    def get_user_url_permissions(self):
        """
        获取 UserInfo 实例直接拥有的URL访问权限
        """
        return _user_get_url_permissions(self, "user")
    
    def get_group_url_permissions(self):
        """
        获取 UserGroup 实例所属 UserGroup 拥有的URL访问权限
        """
        return _user_get_url_permissions(self, "group")
    
    def get_role_url_permissions(self):
        """
        获取 UserGroup 实例所属 Role 拥有的URL访问权限
        """
        return _user_get_url_permissions(self, "role")

    def get_all_url_permissions(self):
        return _user_get_url_permissions(self, 'all')

    def has_urlperm(self, urlperm:str):
        """
        判断指定 UserInfo 实例是否具有特定的URL访问权限
        @urlperm: 权限字符串 <codename>.<url>
        """
        if self.is_active and self.is_superuser:
            return True
        return _user_has_urlperm(self, urlperm)

    def has_urlperms(self, urlperm_list:list):
        """
        如果指定 UserInfo 实例拥有 urlperm_list 中的所有URL访问权限，则返回 True。
        """
        return all(self.has_urlperm(urlperm) for urlperm in urlperm_list)

    def has_module_urlperms(self, url_regex):
        """
        如果指定 UserInfo 实例在指定页面正则表达式上具有访问权限，则返回 True
        @url_regex: URL访问权限对象中，匹配页面的正则表达式。
        """
        if self.is_active and self.is_superuser:
            return True
        return _user_has_module_urlperms(self, url_regex)

    # 获取对象资源权限
    def get_user_obj_permissions(self):
        """
        获取 UserInfo 实例直接拥有的对象资源权限
        """
        return _user_get_obj_permissions(self, "user")

    def get_group_boj_permissions(self):
        """
        获取 UserGroup 实例所属 UserGroup 拥有的对象资源权限
        """
        return _user_get_obj_permissions(self, "group")
    
    def get_role_obj_permissions(self):
        """
        获取 UserGroup 实例所属 Role 拥有的对象资源权限
        """
        return _user_get_obj_permissions(self, "role")

    def get_all_obj_permissions(self):
        return _user_get_obj_permissions(self, "all")

    def has_objperm(self, objperm):
        """
        判断指定 UserInfo 实例是否具有特定的对象资源权限
        """
        if self.is_active and self.is_superuser:
            return True
        return _user_has_objperm(self, objperm)

    def has_objperms(self, objperm_list):
        """
        判断指定 UserInfo 实例是否具有特定的对象资源权限
        @objperm: 权限字符串 <app_label>.<model>.<object_id>.<codename>
        """
        return all(self.has_objperm(objperm) for objperm in objperm_list)

    def has_module_objperms(self, app_label):
        """
        如果指定 UserInfo 实例在指定 Application 上具有对象资源权限，则返回 True
        @app_label: Django Application 标签
        """
        if self.is_active and self.is_superuser:
            return True
        return _user_has_module_objperms(self, app_label)


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

    def has_perm(self, perm, obj = None):
        """
        used for admin customization
        """
        return self.has_objperm(perm)

    def has_perms(self, perm_list, obj = None):
        """
        used for admin customization
        """
        return self.has_objperms(perm_list)
    
    def has_module_perms(self, app_label):
        """
        used for admin customization
        """
        if self.is_active and self.is_superuser:
            return True
        return self.has_module_objperms(app_label)


class LoginLog(models.Model):
    """
    登录日志
    """
    # 删除 UserInfo 时级联删除它的所有登录日志
    user = models.ForeignKey(
        UserInfo, 
        on_delete = models.CASCADE, 
        verbose_name = _("用户账户")
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
        return "<{} Login at {} | {}>".format(self.user, self.login_time, self.ip_address)

# UserInfo 登录后，LoginLog 会自动添加登录信息
@receiver(user_logged_in, sender = UserInfo)
def create_login_log(sender, request, user, **kwargs):
    if "HTTP_X_FORWARDED_FOR" in request.META.keys():
        ip =  request.META["HTTP_X_FORWARDED_FOR"]
    else:
        ip = request.META["REMOTE_ADDR"]
    LoginLog.objects.create(user = user, ip_address = ip)
