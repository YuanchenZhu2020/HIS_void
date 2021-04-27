from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

import his.models as his_model

from rbac import models as rbac_models


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        if 'user_name' in request.session:
            print("session中存在user_name")
            return redirect(reverse("profile"))
        return render(request, IndexView.template_name)


class LoginView(View):
    template_name = "page-login.html"
    user_type = "staff"

    def get(self, request):
        if 'user_name' in request.session:
            print("session中存在user_name")
            return redirect(reverse("profile"))
        return render(request, LoginView.template_name, context={"user_type": "staff"})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = rbac_models.UserInfo.objects.filter(username=username, password=password).first()
        staff = his_model.Staff.objects.filter(user_obj=user).first()
        if user:
            request.session["user_name"] = user.username
            request.session["staff_name"] = staff.name
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


class ForgotPassword(View):
    template_name = "page-forgot-password.html"

    def get(self, request):
        return render(request, ForgotPassword.template_name)

    def post(self, request):
        pass
        return render(request, ForgotPassword.template_name)


class Logout(View):
    def get(self, request):
        del request.session["user_name"]
        return redirect(reverse("index"))


class Profile(View):
    template_name = 'page-profile.html'

    def get(self, request):
        if 'user_name' not in request.session:
            return redirect(reverse("index"))

        # 根据用户名查询需要的信息，用户名通过login传递?
        chang_gui = request.GET.get("chang_gui")
        return render(request, Profile.template_name, locals())

    def post(self, request):
        post_dict = dict(request.POST)

        print("````````````````````````````````````````````````")
        print(post_dict)


class Outpatient(View):
    template_name = 'page-outpatient-workspace.html'

    def get(self, request):
        return render(request, Outpatient.template_name)


class Nurse(View):
    template_name = 'page-nurse-workspace.html'

    def get(self, request):
        return render(request, Nurse.template_name)

class Inspection(View):
    template_name = 'page-inspection-workspace.html'

    def get(self, request):
        return render(request, Inspection.template_name)
