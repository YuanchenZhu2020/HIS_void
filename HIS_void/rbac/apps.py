from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .management import create_urlpermissions


class RbacConfig(AppConfig):
    name = 'rbac'

    def ready(self):
        post_migrate.connect(
            create_urlpermissions,
            dispatch_uid = "HIS_void.rbac.models.create_urlpermissions"
        )
