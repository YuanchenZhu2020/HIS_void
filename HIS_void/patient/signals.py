from django.dispatch import Signal

patient_logged_in = Signal()
patient_login_failed = Signal()
patient_logged_out = Signal()
