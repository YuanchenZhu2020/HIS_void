from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import resolve_url

from .models import PatientUser


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    用来判断用户对象 request.user 是否通过指定测试的装饰器。
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 若通过了测试，即 test_func 返回值为真，则执行传入的视图函数 view_func。
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            # 若没有通过测试，则
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            # 若使用 ajax 进行异步加载，则返回视图函数处理状态 status 以及重定向URL
            # 若不使用 ajax，则直接进行重定向
            if request.is_ajax():
                return JsonResponse(
                    {"status": False, "redirect_url": resolved_login_url}, 
                    safe = False
                )
            else:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(
                    path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def patient_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    患者登录视图函数的装饰器，用于判断患者是否登录，如果没有，则返回登录页面。
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and isinstance(u, PatientUser),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# def permission_required(perm, login_url=None, raise_exception=False):
#     """
#     Decorator for views that checks whether a user has a particular permission
#     enabled, redirecting to the log-in page if necessary.
#     If the raise_exception parameter is given the PermissionDenied exception
#     is raised.
#     """
#     def check_perms(user):
#         if isinstance(perm, str):
#             perms = (perm,)
#         else:
#             perms = perm
#         # First check if the user has the permission (even anon users)
#         if user.has_perms(perms):
#             return True
#         # In case the 403 handler should be called raise the exception
#         if raise_exception:
#             raise PermissionDenied
#         # As the last resort, show the login form
#         return False
#     return user_passes_test(check_perms, login_url=login_url)
