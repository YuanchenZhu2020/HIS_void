from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from rbac.models import URLPermission


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
        user_groups_field = get_user_model()._meta.get_field("groups")
        user_groups_query = "usergroup__{}".format(user_groups_field.related_query_name())
        return URLPermission.objects.filter(**{user_groups_query: user_obj})

    def _get_url_permissions(self, user_obj, from_name):
        """
        返回指定 UserInfo 实例所具有的不同类型的URL访问权限。
        @from_name: 'user' or 'group'
        """
        if not user_obj.is_active or user_obj.is_anonymous:
            return set()

        # URL访问权限缓存字段名称
        urlperm_cache_name = "_%s_urlperm_cache".format(from_name)
        if not hasattr(user_obj, urlperm_cache_name):
            if user_obj.is_superuser:
                perms = URLPermission.objects.all()
            else:
                perms = getattr(self, "_get_{}_url_permissions".format(from_name))(user_obj)
            perms = perms.values_list("codename", "url").order_by()
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

    def get_all_url_permissions(self, user_obj):
        if not user_obj.is_active or user_obj.is_anonymous:
            return set()
        # URL访问权限缓存字段：_urlperm_cache
        if not hasattr(user_obj, "_urlperm_cache"):
            all_perms_set = {
                *self.get_user_url_permissions(user_obj),
                *self.get_group_url_permissions(user_obj),
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
            for perm in self.get_all_permissions(user_obj)
        )

    # Database Objects Access Permission Methods
