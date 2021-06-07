from importlib import import_module

from django.apps import apps as global_apps
from django.conf import settings
from django.db.utils import OperationalError
from django.utils import timezone


# 通过 HIS_void.url 自动添加 URL Permissions
def create_urlpermissions(app_config, add_admin = True, **kwargs):
    #
    if not app_config.models_module:
        return
    # 若 AppConfig 不属于 RBAC Application，则不进行权限检查与创建，避免重复执行
    if app_config != global_apps.get_app_config("rbac"):
        return

    try:
        URLPermission = global_apps.get_model('rbac', 'URLPermission')
        PatientURLPermission = global_apps.get_model('patient', 'PatientURLPermission')
        urlpatterns = import_module(settings.ROOT_URLCONF).urlpatterns
    except LookupError:
        return

    create_time = timezone.now()
    try:
        old_urlps = set(URLPermission.objects.all().values_list("codename", "url_regex"))
        old_patient_urlps = set(PatientURLPermission.objects.all().values_list(
            "url_perm__codename", flat = True
        ))
    except OperationalError:
        return
    new_urlps = set((urlp.pattern.name, urlp.pattern._route) for urlp in urlpatterns)
    # 是否添加管理员页面
    if add_admin:
        new_urlps.add(("admin", "admin/"))
        new_urlps.add(("admin-login", "admin/login/"))
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
    # 修复被级联删除的患者URL访问权限
    # 这里之际使用原有患者URL访问权限生成，需要改为匹配新的URL访问权限来生成
    add_patient_url_perms = [
        PatientURLPermission(
            url_perm = URLPermission.objects.get(codename = cn)
        )
        for cn in old_patient_urlps
    ]
    PatientURLPermission.objects.bulk_create(add_patient_url_perms)

