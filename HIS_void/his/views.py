from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from his.forms import StaffLoginFrom
from rbac.server.init_permission import init_permission


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("profile"))
        else:
            return render(request, IndexView.template_name)


class LoginView(View):
    template_name = "page-login.html"
    user_type = "staff"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("profile"))
        else:
            loginform = StaffLoginFrom()
            context = {"user_type": "staff", "loginform": loginform}
            return render(request, LoginView.template_name, context)

    def post(self, request):
        # 通过 StaffLoginForm.clean() 方法进行多种验证
        login_info = StaffLoginFrom(data = request.POST)
        # 验证成功
        if login_info.is_valid():
            # 获取用户对象和是否保持登录的标识
            user = login_info.get_user()
            remembered = login_info.remembered
            # 登录
            login(request, user)
            # 向 Session 中写入信息
            request.session["username"] = user.get_username()
            # request.session["is_login"] = True
            # 获取用户权限，写入 session 中
            init_permission(request, user)
            # print(request.session["url_key"], request.session["obj_key"])
            # 若选择保持登录，则重新设置 session 保存时间为 1 天 (86400 s)
            if remembered:
                request.session.set_expiry(86400)
            # 浏览器关闭则删除 session
            else:
                request.session.set_expiry(0)
            return redirect(reverse("profile"))
        else:
            error_msg = login_info.errors["__all__"][0]
            loginform = StaffLoginFrom()
            context = {
                "user_type": "staff", 
                "loginform": loginform,
                "error_message": error_msg,
            }
            return render(request, LoginView.template_name, context)


class LogoutView(View):
    template_name = "index"

    def get(self, request):
        logout(request)
        return redirect(reverse(LogoutView.template_name))


class RegisterView(View):
    template_name = "page-register.html"

    def get(self, request):
        return render(request, RegisterView.template_name)

    def post(self, request):
        pass
        return HttpResponse(RegisterView.template_name)


class ForgotPasswordView(View):
    template_name = "page-forgot-password.html"

    def get(self, request):
        return render(request, ForgotPasswordView.template_name)

    def post(self, request):
        pass
        return render(request, ForgotPasswordView.template_name)


class ProfileView(View):
    template_name = 'page-profile.html'

    def get(self, request):
        print("[Session]", request.session)
        if not request.user.is_authenticated:
            return redirect(reverse("index"))
        return render(request, ProfileView.template_name, locals())

    def post(self, request):
        post_dict = dict(request.POST)

        print("````````````````````````````````````````````````")
        print(post_dict)


class OutpatientView(View):
    template_name = 'page-outpatient-workspace.html'

    def get(self, request):
        return render(request, OutpatientView.template_name)
