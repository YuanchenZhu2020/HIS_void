from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from patient import login, init_patient_url_permission
from patient.forms import PatientLoginFrom


class PatientLoginView(View):
    template_name = "page-login.html"
    patient_next_url_name = "patient-user"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse(PatientLoginView.patient_next_url_name))
        else:
            loginform = PatientLoginFrom()
            context = {"user_type": "patient", "loginform": loginform}
            return render(request, PatientLoginView.template_name, context)

    def post(self, request):
        # 通过 PatientLoginForm.clean() 方法进行多种验证
        login_info = PatientLoginFrom(data = request.POST)
        # 验证成功
        if login_info.is_valid():
            # 获取用户对象和是否保持登录的标识
            user = login_info.get_user()
            remember_me = login_info.remember_me
            # 登录
            login(request, user)
            # 向 Session 中写入信息
            request.session["patient_id"] = user.get_patient_id()
            # request.session["is_login"] = True
            # 获取用户权限，写入 session 中
            init_patient_url_permission(request, user)
            # print(request.session["url_key"], request.session["obj_key"])
            # 若选择保持登录，则重新设置 session 保存时间为 1 天 (86400 s)
            if remember_me:
                request.session.set_expiry(86400)
            # 浏览器关闭则删除 session
            else:
                request.session.set_expiry(0)
            print("[Patient Login View]", request.user)
            return redirect(reverse(PatientLoginView.patient_next_url_name))
        else:
            error_msg = login_info.errors["__all__"][0]
            loginform = PatientLoginFrom()
            context = {
                "user_type": "patient", 
                "loginform": loginform,
                "error_message": error_msg,
            }
            return render(request, PatientLoginView.template_name, context)


class PatientWorkSpaceView(View):
    template_name = "patient-view.html"
    patient_next_url_name = "index"

    def get(self, request):
        print("[Patient Workspace View]", request.user)
        if request.user.is_authenticated:
            context = {"user_type": "patient"}
            return render(request, PatientWorkSpaceView.template_name, context = context)
        else:
            # print(type(request.user))
            return redirect(reverse(PatientWorkSpaceView.patient_next_url_name))

    # def post(self, request):
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")
    #     # 测试用
    #     print(username, password)
    #     if username == "test" and password == "123456":
    #         return redirect(reverse("index"))
    #     else:
    #         context = {"user_type": "patient", "name_or_password_error": True}
    #         return render(request, PatientLoginView.template_name, context)


class PatientWorkMyView(View):
    template_name = "patient-my.html"

    def get(self, request):
        return render(request, PatientWorkMyView.template_name, context={"user_type": "patient"})
