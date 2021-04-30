from django.apps import AppConfig
from django.db.models.query_utils import DeferredAttribute

from . import get_user_model
from .signals import patient_logged_in


class PatientConfig(AppConfig):
    name = 'patient'

    def ready(self):
        last_login_field = getattr(get_user_model(), "last_login", None)
        # Register the handler only if UserModel.last_login is a field.
        if isinstance(last_login_field, DeferredAttribute):
            from .models import update_last_login
            patient_logged_in.connect(update_last_login, dispatch_uid = "update_last_login")
