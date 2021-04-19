from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

# import his.models as his_models
# import rbac.models as rbac_models


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        # if "user_name" in request.session:
        #     print("session中存在user_name")
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
            context = {"user_type": "staff"}
            return render(request, LoginView.template_name, context)

    def post(self, request):
        # 获取用户验证所需信息
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 用户验证
        user = authenticate(request, username = username, password = password)
        # 验证成功，向 Session 中写入信息
        if user is not None:
            login(request, user)
            request.session["username"] = user.get_username()
            request.session["is_login"] = True
            return redirect(reverse("profile"))
        else:
            context = {"user_type": "staff", "name_or_password_error": True}
            return render(request, LoginView.template_name, context)


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


class LogoutView(View):
    def get(self, request):
        request.session.clear()
        return redirect(reverse("index"))


class ProfileView(View):
    template_name = 'page-profile.html'

    def get(self, request):
        print("[Session]", request.session)
        if not request.session["is_login"]:
            return redirect(reverse("index"))

        # 根据用户名查询需要的信息，用户名通过login传递?
        chang_gui = request.GET.get("chang_gui")
        return render(request, ProfileView.template_name, locals())

    def post(self, request):
        post_dict = dict(request.POST)

        print("````````````````````````````````````````````````")
        print(post_dict)


class OutpatientView(View):
    template_name = 'page-outpatient-workspace.html'

    def get(self, request):
        return render(request, OutpatientView.template_name)
