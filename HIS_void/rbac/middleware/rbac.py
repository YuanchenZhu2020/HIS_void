from django.conf import settings
from django.shortcuts import HttpResponse, redirect
from django.urls import reverse

import re

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
    count = 0
    """
    process_request: 接收到用户请求，执行视图函数前运行。
        return: [] None HttpResponse
    判断用户对于当前访问的 URL 是否具有权限。
    如果有权限则返回 None，没有则返回 HttpResponse 对象
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.count += 1
        response = None
        if hasattr(self, "process_request"):
            print("[middleware] process request")
            response = self.process_request(request)
        if not response:
            print("[middleware] get response")
            response = self.get_response(request)
        return response

    def process_request(self, request):
        """
        在执行视图函数之前判断用户能否访问该页面。
        """
        request_url = request.path_info
        print('【request_url】 ', request_url)
        permission_url = request.session.get(settings.PERMISSION_URL_KEY)
        print('【permission_url】 ', permission_url)

        # Cond 1: 超级用户，具有完全权限
        if request.user.is_superuser:
            return None
        # Cond 2: URL 白名单
        for url in settings.SAFE_URL:
            if re.match(url, request_url):
                print("第", self.count, "调用中间件")
                print("··········匹配成功·············")
                return None
        # Cond 3: 用户未登入
        if not permission_url:
            print("第", self.count, "调用中间件")
            print("重定向到index")
            return redirect(reverse("index"))
            pass
        # Cond 4: 一般情况
        flag = False
        for perm_group_id, code_url in permission_url.items():
            for url in code_url["urls"]:
                url_pattern = "^{}$".format(url)
                if re.match(url_pattern, request_url):
                    request.session["permission_codes"] = code_url["codes"]
                    flag = True
                    break
        if not flag:
            # 测试使用
            if settings.DEBUG:
                info = "<br/>" + ("<br/>".join(code_url["urls"]))
                return HttpResponse("无访问权限，尝试以下网址： {}".format(info))
            else:
                return HttpResponse("无权限访问")
