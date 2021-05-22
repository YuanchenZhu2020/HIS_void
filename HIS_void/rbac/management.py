from importlib import import_module

from django.apps import apps as global_apps
from django.conf import settings
from django.db.utils import OperationalError
from django.utils import timezone


# 通过 HIS_void.url 自动添加 URL Permissions
def create_urlpermissions(app_config, **kwargs):
    # 
    if not app_config.models_module:
        return
    # 若 AppConfig 不属于 RBAC Application，则不进行权限检查与创建，避免重复执行
    if app_config != global_apps.get_app_config("rbac"):
        return

    try:
        URLPermission = global_apps.get_model('rbac', 'URLPermission')
        urlpatterns = import_module(settings.ROOT_URLCONF).urlpatterns
    except LookupError:
        return

    create_time = timezone.now()
    try:
        old_urlps = set(URLPermission.objects.all().values_list("codename", "url_regex"))
    except OperationalError:
        return
    new_urlps = set((urlp.pattern.name, urlp.pattern._route) for urlp in urlpatterns)
    # 删除被删除的URL对应的URL访问权限
    delete_urlperms = old_urlps - new_urlps
    delete_urls = [nu[1] for nu in delete_urlperms]
    URLPermission.objects.filter(url_regex__in = delete_urls).delete()
    # 添加新增的URL对应的URL访问权限
    add_urlps = new_urlps - old_urlps
    if len(add_urlps) > 0:
        add_url_objs = [
            URLPermission(
                codename = urlp[0],
                url_regex = '/' + urlp[1],
                create_time = create_time
            )
            for urlp in add_urlps
            if urlp[0] is not None
        ]
        URLPermission.objects.bulk_create(add_url_objs)
