from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from patient import login, init_patient_url_permission
from patient.forms import PatientLoginForm, PatientRegisterForm
from patient.models import PatientUser
from externalapi.external_api import IDInfoQuery


class PatientLoginView(View):
    template_name = "page-login.html"
    patient_next_url_name = "patient-user"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse(PatientLoginView.patient_next_url_name))
        else:
            loginform = PatientLoginForm()
            context = {"user_type": "patient", "loginform": loginform}
            return render(request, PatientLoginView.template_name, context)

    def post(self, request):
        # 通过 PatientLoginForm.clean() 方法进行多种验证
        login_info = PatientLoginForm(data = request.POST)
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
            loginform = PatientLoginForm()
            context = {
                "user_type": "patient", 
                "loginform": loginform,
                "error_message": error_msg,
            }
            return render(request, PatientLoginView.template_name, context)


class PatientRegisterView(View):
    template_name = "page-register.html"
    patient_next_url_name = "login-patient"

    def get(self, request):
        registerform = PatientRegisterForm()
        context = {"registerform": registerform}
        return render(request, PatientRegisterView.template_name, context = context)

    def post(self, request):
        register_info = PatientRegisterForm(data = request.POST)
        if register_info.is_valid():
            # print(register_info.__dict__)
            data = register_info.cleaned_data
            id_type = data.get("id_type")
            id_number = data.get("id_number")
            phone = data.get("phone")
            user = PatientUser.objects.filter(
                id_type = id_type, 
                id_number = id_number
            ).first()
            if not user:
                user = PatientUser(
                    id_type = id_type,
                    id_number = id_number,
                    phone = phone
                )
                user.set_password(data.get("password1"))
                id_info_query = IDInfoQuery(user.id_number)
                user.set_name(id_info_query.get_name())
                user.set_gender(id_info_query.get_gender())
                user.set_birthday(id_info_query.get_birthday())
                user.save()
                return redirect(reverse(PatientRegisterView.patient_next_url_name))
        # 表单数据验证失败
        if not register_info.is_valid():
            # print(register_info.__dict__)
            error_msg = list(register_info.errors.values())[0]
        # 已存在与已填写信息对应的患者用户
        if user:
            error_msg = "用户已注册"
        loginform = PatientRegisterForm()
        context = {
            "registerform": loginform,
            "error_message": error_msg,
        }
        return render(request, PatientRegisterView.template_name, context)


class ForgotPasswordView(View):
    template_name = "page-forgot-password.html"

    def get(self, request):
        return render(request, ForgotPasswordView.template_name)

    def post(self, request):
        pass
        return render(request, ForgotPasswordView.template_name)


class PatientWorkSpaceView(View):
    template_name = "patient-view.html"
    patient_next_url_name = "index"

    def get(self, request):
        print("[Patient Workspace View]", request.user)
        if request.user.is_authenticated  and isinstance(request.user, PatientUser):
            context = {"user_type": "patient"}
            return render(request, PatientWorkSpaceView.template_name, context = context)
        else:
            # print(type(request.user))
            return redirect(reverse(PatientWorkSpaceView.patient_next_url_name))


class PatientWorkMyView(View):
    template_name = "patient-my.html"

    def get(self, request):
        return render(request, PatientWorkMyView.template_name, context={"user_type": "patient"})
