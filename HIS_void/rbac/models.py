from django.db import models


# class Menu(models.Model):
#     title = models.CharField(max_length = 32, unique = True, verbose_name = "一级菜单")

#     class Meta:
#         verbose_name = "一级菜单表"
#         verbose_name_plural = verbose_name
    
#     def __str__(self) -> str:
#         return "<Menu {}>".format(self.title)


class PermGroup(models.Model):
    title       = models.CharField(max_length = 32, verbose_name = "权限组名称")
    create_time = models.DateTimeField(auto_now_add = True, editable = False, verbose_name = "创建时间")
    # menu  = models.ForeignKey(Menu, blank = True, on_delete = models.CASCADE, verbose_name = "所属菜单")

    class Meta:
        verbose_name = "权限组表"
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
        verbose_name = "权限表"
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
        verbose_name = "角色表"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return "<Role {}>".format(self.title)


class UserInfo(models.Model):
    # 以 6 位数字的工号作为登录账号
    # 患者账号单独管理
    username    = models.CharField(max_length = 6, verbose_name = "登录账号")
    password    = models.CharField(max_length = 256, verbose_name = "登录密码")
    create_time = models.DateTimeField(auto_now_add = True, editable = False, verbose_name = "创建时间")
    roles       = models.ManyToManyField(Role, verbose_name = "用户角色")

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return "<User {}>".format(self.username)
