import re

from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse

from rbac.models import URLPermission

"""
|
| process_request()
| process_view(
|    view()
| )
| process_template_response()
| process_response()
|
- process_exception()
"""


class RBACMiddleware:
    """
    process_request: 接收到用户请求，执行视图函数前运行。
        return: [] None HttpResponse
    判断用户对于当前访问的 URL 是否具有权限。
    如果有权限则返回 None，没有则返回 HttpResponse 对象
    """
    page_404 = "page-error-404.html"
    page_403 = "page-error-403.html"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # self.count += 1
        response = None
        if hasattr(self, "process_request"):
            # print("[middleware] process request")
            response = self.process_request(request)
        if not response:
            # print("[middleware] get response")
            response = self.get_response(request)
        return response

    def process_request(self, request):
        """
        在执行视图函数之前判断用户能否访问该页面。
        """
        request_url = request.path_info
        url_permissions = request.session.get(settings.PERMISSION_URL_KEY)
        obj_permissions = request.session.get(settings.PERMISSION_OBJ_KEY)
        # print("[middleware]", request.user)
        print("\033[1;33m[request_url]\033[0m", request_url)
        print("\033[1;33m[url_permissions]\033[0m", url_permissions)
        print("\033[1;33m[obj permissions]\033[0m", obj_permissions)
        # 获取所有可用的 URL
        all_urls = URLPermission.objects.values_list("url_regex", flat = True)
        
        # Cond 0: 超级用户，具有完全权限
        if hasattr(request.user, "is_superuser") \
            and request.user.is_superuser:
            print("\033[1;31m[RBAC Cond 0]\033[0m")
            return None
        # Cond 1: 访问页面不存在
        # print(list(all_urls))
        if request_url not in all_urls:
            print("\033[1;31m[RBAC Cond 1]\033[0m")
            return render(request, RBACMiddleware.page_404)
        # Cond 2: URL 白名单
        for url in settings.SAFE_URL:
            url_pattern = "^{}$".format(url)
            if re.match(url_pattern, request_url):
                # print("第", self.count, "调用中间件")
                # print("··········匹配成功·············")
                print("\033[1;31m[RBAC Cond 2]\033[0m")
                return None
        # Cond 3: 用户未登入
        if not url_permissions:
            # print("第", self.count, "调用中间件")
            print("\033[1;31m[RBAC Cond 3]\033[0m")
            return redirect(reverse("index"))
        # Cond 4: 一般情况
        flag = False
        # 遍历用户可访问URL
        for code_name, url in url_permissions:
            url_pattern = "^{}$".format(url)
            if re.match(url_pattern, request_url):
                print("\033[1;31m[RBAC Cond 4]\033[0m")
                flag = True
                break
        if not flag:
            # 测试使用
            if settings.DEBUG:
                code_urls = [item[-1] for item in url_permissions]
                info = "<br/>" + ("<br/>".join(code_urls))
                return HttpResponse("无访问权限，尝试以下网址： {}".format(info))
            else:
                return render(request, RBACMiddleware.page_403)
