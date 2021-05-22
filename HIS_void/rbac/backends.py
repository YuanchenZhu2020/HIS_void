from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from rbac.models import ObjectPermission, URLPermission, UserGroup


class CustomBackends(ModelBackend):
    # URL Access Permission Methods

    def _get_user_url_permissions(self, user_obj):
        """
        获取 UserInfo 直接拥有的所有URL访问权限。
        """
        return user_obj.url_permissions.all()
    
    def _get_group_url_permissions(self, user_obj):
        """
        获取 UserInfo 所属 UserGroup 用户组拥有的所有URL访问权限：
            1. 获取 settings.AUTH_USER_MODEL 代表的对象（UserInfo）
            2. 获取 UserInfo 的 groups 属性（UserGroup）
            3. 构造查询条件的名称：<表名>__<related_query_name>
            4. 在 URLPermission 表中进行条件查询（使用**构造查询表达式）
        """
        # URLPermission <- UserGroup <- UserInfo
        user_groups_field = get_user_model()._meta.get_field("groups")
        user_groups_query = "usergroups__{}".format(user_groups_field.related_query_name())
        group_url_perms_queryset =  URLPermission.objects.filter(**{user_groups_query: user_obj})
        # URLPermission <- Role <- (UserGroup <- UserInfo)
        usergroups = UserGroup.objects.filter(users = user_obj)
        for ug in usergroups:
            group_roles_field = ug._meta.get_field("roles")
            group_roles_query = "roles__{}".format(group_roles_field.related_query_name())
            group_url_perms_queryset |= URLPermission.objects.filter(**{group_roles_query: ug})
        return group_url_perms_queryset

    def _get_role_url_permissions(self, user_obj):
        """
        获取 UserInfo 所属 Role 角色拥有的所有URL访问权限：
            1. 获取 settings.AUTH_USER_MODEL 代表的对象（UserInfo）
            2. 获取 UserInfo 的 roles 属性（Role）
            3. 构造查询条件的名称：<表名>__<related_query_name>
            4. 在 URLPermission 表中进行条件查询（使用**构造查询表达式）
        """
        user_roles_field = get_user_model()._meta.get_field("roles")
        user_roles_query = "roles__{}".format(user_roles_field.related_query_name())
        return URLPermission.objects.filter(**{user_roles_query: user_obj})

    def _get_url_permissions(self, user_obj, from_name):
        """
        返回指定 UserInfo 实例所具有的不同类型的URL访问权限。
        @from_name: 'user' or 'group' or 'role'
        """
        if not user_obj.is_active or user_obj.is_anonymous:
            return set()

        # URL访问权限缓存字段名称
        urlperm_cache_name = "_{}_urlperm_cache".format(from_name)
        if not hasattr(user_obj, urlperm_cache_name):
            if user_obj.is_superuser:
                perms = URLPermission.objects.all()
            else:
                perms = getattr(self, "_get_{}_url_permissions".format(from_name))(user_obj)
            perms = perms.values_list("codename", "url_regex").order_by()
            # 设置URL访问权限缓存
            setattr(user_obj, urlperm_cache_name, {"{}.{}".format(cn, url) for cn, url in perms})
        return getattr(user_obj, urlperm_cache_name)

    def get_user_url_permissions(self, user_obj):
        """
        返回URL访问权限字符串集合（User直接持有）
        """
        return self._get_url_permissions(user_obj, "user")

    def get_group_url_permissions(self, user_obj):
        """
        返回URL访问权限字符串集合（User通过Group持有）
        """
        return self._get_url_permissions(user_obj, "group")

    def get_role_url_permissions(self, user_obj):
        """
        返回URL访问权限字符串集合（User通过Role持有）
        """
        return self._get_url_permissions(user_obj, "role")

    def get_all_url_permissions(self, user_obj):
        if not user_obj.is_active or user_obj.is_anonymous:
            return set()
        # URL访问权限缓存字段：_urlperm_cache
        if not hasattr(user_obj, "_urlperm_cache"):
            all_perms_set = {
                *self.get_user_url_permissions(user_obj),
                *self.get_group_url_permissions(user_obj),
                *self.get_role_url_permissions(user_obj),
            }
            user_obj._urlperm_cache = all_perms_set
        return user_obj._urlperm_cache

    def has_urlperm(self, user_obj, urlperm):
        """
        判断指定 UserInfo 实例是否具有特定的URL访问权限
        @urlperm: 权限字符串 <codename>.<url>
        """
        return user_obj.is_active and urlperm in self.get_all_url_permissions(user_obj)

    def has_module_urlperms(self, user_obj, url_regex):
        """
        如果指定 UserInfo 实例在指定页面正则表达式上具有访问权限，则返回 True
        @url_regex: URL访问权限对象中，匹配页面的正则表达式。
        """
        return user_obj.is_active and any(
            perm[perm.index('.'):] == url_regex
            for perm in self.get_all_url_permissions(user_obj)
        )

    # Database Objects Access Permission Methods

    def _get_user_obj_permissions(self, user_obj):
        """
        获取 UserInfo 直接拥有的所有兑现资源权限。
        """
        return user_obj.obj_permissions.all()
    
    def _get_group_obj_permissions(self, user_obj):
        """
        获取 UserInfo 所属 UserGroup 用户组拥有的所有对象资源权限：
            1. 获取 settings.AUTH_USER_MODEL 代表的对象（UserInfo）
            2. 获取 UserInfo 的 groups 属性（UserGroup）
            3. 构造查询条件的名称：<表名>__<related_query_name>
            4. 在 ObjectPermission 表中进行条件查询（使用**构造查询表达式）
        """
        # ObjectPermission <- UserGroup <- UserInfo
        user_groups_field = get_user_model()._meta.get_field("groups")
        user_groups_query = "usergroups__{}".format(user_groups_field.related_query_name())
        group_obj_perms_queryset = ObjectPermission.objects.filter(**{user_groups_query: user_obj})
        # URLPermission <- Role <- (UserGroup <- UserInfo)
        usergroups = UserGroup.objects.filter(users = user_obj)
        for ug in usergroups:
            group_roles_field = ug._meta.get_field("roles")
            group_roles_query = "roles__{}".format(group_roles_field.related_query_name())
            group_obj_perms_queryset |= ObjectPermission.objects.filter(**{group_roles_query: ug})
        return group_obj_perms_queryset

    def _get_role_obj_permissions(self, user_obj):
        """
        获取 UserInfo 所属 Role 角色拥有的所有对象资源权限：
            1. 获取 settings.AUTH_USER_MODEL 代表的对象（UserInfo）
            2. 获取 UserInfo 的 roles 属性（Role）
            3. 构造查询条件的名称：<表名>__<related_query_name>
            4. 在 ObjectPermission 表中进行条件查询（使用**构造查询表达式）
        """
        user_roles_field = get_user_model()._meta.get_field("roles")
        user_roles_query = "roles__{}".format(user_roles_field.related_query_name())
        return ObjectPermission.objects.filter(**{user_roles_query: user_obj})

    def _get_obj_permissions(self, user_obj, from_name):
        """
        返回指定 UserInfo 实例所具有的不同类型的对象资源权限。
        @from_name: 'user' or 'group' or 'role'
        """
        if not user_obj.is_active or user_obj.is_anonymous:
            return set()

        # 对象资源权限缓存字段名称
        # Format: <app_label>.<model>.<object_id>.<codename>
        objperm_cache_name = "_{}_objperm_cache".format(from_name)
        if not hasattr(user_obj, objperm_cache_name):
            if user_obj.is_superuser:
                perms = ObjectPermission.objects.all()
            else:
                perms = getattr(self, "_get_{}_obj_permissions".format(from_name))(user_obj)
                # print(perms)
            perms = perms.values_list(
                "permission__content_type__app_label",
                "permission__content_type__model",
                "object_id", 
                "permission__codename", 
            ).order_by()
            # 设置对象资源权限缓存
            setattr(
                user_obj, 
                objperm_cache_name, 
                {"{}.{}.{}.{}".format(al, mo, oid, cn) for al, mo, oid, cn in perms}
            )
        return getattr(user_obj, objperm_cache_name)

    def get_user_obj_permissions(self, user_obj):
        """
        返回对象资源权限字符串集合（User直接持有）
        """
        return self._get_obj_permissions(user_obj, "user")

    def get_group_obj_permissions(self, user_obj):
        """
        返回对象资源权限字符串集合（User通过Group持有）
        """
        return self._get_obj_permissions(user_obj, "group")

    def get_role_obj_permissions(self, user_obj):
        """
        返回对象资源权限字符串集合（User通过Role持有）
        """
        return self._get_obj_permissions(user_obj, "role")

    def get_all_obj_permissions(self, user_obj):
        if not user_obj.is_active or user_obj.is_anonymous:
            return set()
        # URL访问权限缓存字段：_objerm_cache
        if not hasattr(user_obj, "_objerm_cache"):
            all_perms_set = {
                *self.get_user_obj_permissions(user_obj),
                *self.get_group_obj_permissions(user_obj),
                *self.get_role_obj_permissions(user_obj),
            }
            user_obj._objperm_cache = all_perms_set
        return user_obj._objperm_cache

    def has_objperm(self, user_obj, objperm):
        """
        判断指定 UserInfo 实例是否具有特定的对象资源权限
        @objperm: 权限字符串 <app_label>.<model>.<object_id>.<codename>
        """
        return user_obj.is_active and objperm in self.get_all_obj_permissions(user_obj)

    def has_module_objperms(self, user_obj, app_label):
        """
        如果指定 UserInfo 实例在指定 Application 上具有对象资源权限，则返回 True
        @app_label: Django Application 标签
        """
        return user_obj.is_active and any(
            perm[:perm.index('.')] == app_label
            for perm in self.get_all_obj_permissions(user_obj)
        )
