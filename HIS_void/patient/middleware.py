from django.contrib.auth.models import AnonymousUser

from . import get_user as get_patient_user


def get_user(request):
    request._cached_user = get_patient_user(request)
    return request._cached_user


class PatientUserMiddleware:
    """
    AuthenticationMiddleware 无法获取 PatientUser 对象，因此
    每次访问页面都会将 request.user 覆写为 AnonymousUser。

    PatientUserMiddleware 的作用就是在  AuthenticationMiddleware
    运行之后，重新将对应的 PatientUser 写入 request.user。

    **注意**：在 settings 中的 Middleware，PatientUserMiddleware
    应该放在 AuthenticationMiddleware 之后，RBACMiddleware 之前。
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if hasattr(self, "process_request"):
            # print("[patient middleware] process request")
            response = self.process_request(request)
        if not response:
            # print("[patient middleware] get response")
            response = self.get_response(request)
        return response

    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        # print(request.user)
        # print(type(request.user))
        # print(isinstance(request.user, AnonymousUser))
        if isinstance(request.user, AnonymousUser):
            request.user = get_user(request)
