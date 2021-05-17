from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from patient import login, init_patient_url_permission
from patient.forms import PatientLoginForm, PatientRegisterForm
from patient.models import PatientUser
from externalapi.external_api import IDInfoQuery


class PatientLoginView(View):
    template_name = "page-login.html"
    patient_next_url_name = "patient"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse(PatientLoginView.patient_next_url_name))
        else:
            loginform = PatientLoginForm()
            context = {"user_type": "patient", "loginform": loginform}
            return render(request, PatientLoginView.template_name, context)

    def post(self, request):
        # 通过 PatientLoginForm.clean() 方法进行多种验证
        login_info = PatientLoginForm(data=request.POST)
        # 验证成功
        if login_info.is_valid():
            # 获取用户对象和是否保持登录的标识
            user = login_info.get_user()
            remember_me = login_info.remember_me
            # 登录
            login(request, user)
            # 向 Session 中写入信息
            request.session["patient_id"] = user.get_patient_id()
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
    patient_next_url_name = "register-success"

    def get(self, request):
        registerform = PatientRegisterForm()
        context = {"registerform": registerform}
        return render(request, PatientRegisterView.template_name, context=context)

    def post(self, request):
        register_info = PatientRegisterForm(data=request.POST)
        # 表单数据验证成功
        if register_info.is_valid():
            # print(register_info.__dict__)
            data = register_info.cleaned_data
            id_type = data.get("id_type")
            id_number = data.get("id_number")
            phone = data.get("phone")
            user_reg = PatientUser.objects.filter(
                id_type=id_type,
                id_number=id_number
            ).first()
            # 没有找到注册用户（即能够注册）
            if not user_reg:
                user = PatientUser(
                    id_type=id_type,
                    id_number=id_number,
                    phone=phone
                )
                user.set_password(data.get("password1"))
                id_info_query = IDInfoQuery(user.id_number)
                user.set_name(id_info_query.get_name())
                user.set_gender(id_info_query.get_gender())
                user.set_birthday(id_info_query.get_birthday())
                user.save()
                # 注册成功，将必要信息写入session，跳转到账户信息页面
                request.session["register_user_info"] = {
                    "就诊号": user.patient_id,
                    "证件类型": user.get_id_type_display(),
                    "证件号": user.id_number,
                    "姓名": user.name,
                    "性别": user.get_gender_display(),
                    "出生日期": user.birthday.strftime("%Y-%m-%d"),
                    "手机号码": user.phone,
                    "注册时间": user.create_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                return redirect(reverse(PatientRegisterView.patient_next_url_name))
            # 已存在与已填写信息对应的患者用户
            else:
                error_msg = "用户已注册"
        # 表单数据验证失败
        else:
            # print(register_info.__dict__)
            error_msg = list(register_info.errors.values())[0]
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


class PatientView(View):
    template_name = "patient.html"
    patient_next_url_name = "index"

    def get(self, request):
        print("[Patient Workspace View]", request.user)
        # if request.user.is_authenticated  and isinstance(request.user, PatientUser):
        #     context = {"user_type": "patient"}
        #     return render(request, PatientView.template_name, context = context)
        # else:
        #     # print(type(request.user))
        #     return redirect(reverse(PatientView.patient_next_url_name))

        '''
        需要所有可以用于挂号的科室信息
        '''
        KSdata = [{
            "id": "1",  # 挂号的序号
            "name": "内科",
        }, {
            "id": "2",  # 挂号的序号
            "name": "呼吸科",
        }, {
            "id": "3",  # 挂号的序号
            "name": "小儿科",
        }, {
            "id": "4",  # 挂号的序号
            "name": "牙科",
        }, {
            "id": "5",  # 挂号的序号
            "name": "精神科",
        }, {
            "id": "6",  # 挂号的序号
            "name": "外科",
        }, ]

        '''
        需要可选的所有挂号日期
        '''
        ALTDates = ["5-15", "5-16", '5-17', '5-18', '5-19', '5-20', '5-21']
        return render(request, PatientView.template_name, locals())
        # print("[Patient Workspace View]", request.user)
        # if request.user.is_authenticated and isinstance(request.user, PatientUser):
        #     context = {"user_type": "patient"}
        #     return render(request, PatientView.template_name, context=context)
        # else:
        #     # print(type(request.user))
        #     return redirect(reverse(PatientView.patient_next_url_name))


class PatientRegisterSuccessView(View):
    template_name = "register-success.html"

    def get(self, request):
        account_info = request.session.get("register_user_info")
        login_name = None
        if account_info:
            login_name = str(account_info["就诊号"]).rjust(6, '0')
        context = {
            "account_info": account_info,
            "login_name": login_name
        }
        # 清除 session 中的账户信息
        if context["account_info"]:
            del request.session["register_user_info"]
        return render(request, PatientRegisterSuccessView.template_name, context=context)


class PatientDetailsView(View):
    template_name = "patient-details.html"

    def get(self, request):
        user_type = {"user_type": "patient"}  # 这个是用来干嘛的

        # 我想在这里得到主页的登录人的信息（以下所有查询的基础）怎么办，如何判断是否登录，以及对登录人进行限制操作

        # 待诊信息_需要从数据库查询，以下给出范例
        '''
        需要医生的主键信息（用于再次预约）
        '''
        DZdata = [{
            "number": "1234",  # 挂号的序号
            "keshi": "内科",
            "menzhen": "呼吸门诊",
            "doctor_name": "A医生",
            "date": "2021-01-01",
            "time": "15:00",
        }, {
            "number": "124",  # 挂号的序号
            "keshi": "内科",
            "menzhen": "呼吸门诊",
            "doctor_name": "B医生",
            "date": "2021-01-01",
            "time": "15:00",
        }, ]

        # 当前就诊信息_需要从数据库查询，以下给出范例
        '''
        需要当前就诊的主键信息
        '''
        DQJZdata = [{
            "id": "123",
            "name": "CT1",
            "location": "综合二层102",
            "order": 189,
            "status": "等待检查",
        }, {
            "id": "444",
            "name": "CT2",
            "location": "综合二层102",
            "order": 199,
            "status": "等待检查",
        },
        ]

        # 确诊记录_需要从数据库查询，以下给出范例
        '''
        需要确诊记录的主键信息；医生的主键信息（用于再次预约）
        '''
        QZdata = [{
            "id": "123",
            "date": "2020-4-9",
            "doctor": "A医生",
            "quezhen": "肺炎",
        }, {
            "id": "333",
            "date": "2020-4-9",
            "doctor": "B医生",
            "quezhen": "感冒",
        }, ]

        # 检查记录
        '''
        需要检查记录的主键信息
        '''
        JCdata = [{
            "id": "111",
            "name": "B超",
            "price": "199",
        }, {
            "id": "222",
            "name": "CT",
            "price": "199",
        }, ]

        # 登录人个人信息
        return render(request, PatientDetailsView.template_name, locals())
