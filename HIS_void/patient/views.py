from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from patient import login, init_patient_url_permission
from patient.forms import PatientLoginForm, PatientRegisterForm
from patient.models import PatientUser
from his.models import Department
from laboratory.models import PatientTestItem
from outpatient.models import RemainingRegistration, RegistrationInfo
from patient.decorators import patient_login_required
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
            request.session["name"] = user.name
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
    # patient_next_url_name = "index"

    DEPT_DATA_CACHE = None
    REG_DATES_CACHE = None
    UPDATE_DATE = None    

    def get(self, request):
        print("[Patient Workspace View]", request.user)
        # 从缓存获取可挂号科室与挂号日期
        if PatientView.UPDATE_DATE is None or PatientView.UPDATE_DATE < timezone.localdate():
            # 挂号科室
            depts = Department.objects.filter(
                accept_patient = 1
            ).values_list("usergroup__ug_id", "usergroup__name")
            PatientView.DEPT_DATA_CACHE = [
                {"id": dept[0], "name": dept[1]}
                for dept in depts
            ]
            # 挂号日期
            reg_dates = RemainingRegistration.objects.all().values_list(
                "register_date"
            ).distinct().order_by("register_date")
            reg_dates = sorted(set([date[0].strftime("%Y-%m-%d") for date in reg_dates]))
            PatientView.REG_DATES_CACHE = reg_dates
            # 更新缓存日期
            PatientView.UPDATE_DATE = timezone.localdate()
        context = {
            "DeptsData": PatientView.DEPT_DATA_CACHE,
            "RegDates": PatientView.REG_DATES_CACHE
        }
        return render(request, PatientView.template_name, context = context)


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


@method_decorator(patient_login_required(login_url = "/login-patient"), name = "get")
class PatientDetailsView(View):
    template_name = "patient-details.html"

    def get(self, request):
        patient_id = request.session["patient_id"]
        patient = PatientUser.objects.get_by_patient_id(patient_id)
        # 历史就诊
        # 数据格式示例：[{
        #     "number": "1234",  # 挂号的序号
        #     "keshi": "内科",
        #     "menzhen": "呼吸门诊",
        #     "doctor_id": "000001",
        #     "doctor_name": "A医生",
        #     "date": "2021-01-01",
        #     "time": "15:00",
        # },...]

        # 当前就诊信息
        '''
        需要当前就诊的主键信息
        '''
        # 数据格式示例：[{
        #     "id": "444",
        #     "name": "CT2",
        #     "location": "综合二层102",
        #     "order": 199,
        #     "status": "等待检查",
        # },...]
        # waiting_diag_data = 
        waiting_diagnosis = []

        # 确诊记录
        # 数据格式示例：[{
        #     "reg_id": "333",
        #     "date": "2020-4-9",
        #     "doctor_id": "000001",
        #     "doctor_name": "B医生",
        #     "diagnosis_results": "感冒",
        # },...]
        history_regs = RegistrationInfo.objects.filter(
            patient = patient,
            diagnosis_results__isnull = False,
        ).order_by(
            "-reg_id"
        ).values_list(
            "reg_id", "registration_date__date", 
            "medical_staff__user__username", "medical_staff__name", 
            "diagnosis_results"
        )
        diagnosis_data = []
        for history_reg in history_regs:
            diagnosis_data.append(dict(zip(
                ["reg_id", "date", "doctor_id", "doctor_name", "diagnosis_result"],
                history_reg
            )))
        # 检查记录
        # 数据格式示例：[{
        #     "id": "111",
        #     "name": "B超",
        #     "price": "199",
        # },...]
        history_tests = PatientTestItem.objects.filter(
            registration_info__patient = patient
        ).order_by(
            "-test_id"
        ).values_list(
            "test_id", "issue_time", 
            "test_item__inspect_name", "test_results",
        )
        tests_data = []
        for history_test in history_tests:
            tests_data.append(dict(zip(
                ["test_id", "date", "name", "result"], history_test
            )))

        # 登录人个人信息
        context = {
            "diagnosis_data": diagnosis_data,
            "tests_data": tests_data,
        }
        return render(request, PatientDetailsView.template_name, locals())
