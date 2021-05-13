from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from patient import login, init_patient_url_permission
from patient.forms import PatientLoginFrom
from patient.models import PatientUser


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
        login_info = PatientLoginFrom(data=request.POST)
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


class PatientWorkSpaceView(View):
    template_name = "patient-view.html"
    patient_next_url_name = "index"

    def get(self, request):
        print("[Patient Workspace View]", request.user)
        if request.user.is_authenticated and isinstance(request.user, PatientUser):
            context = {"user_type": "patient"}
            return render(request, PatientWorkSpaceView.template_name, context=context)
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
    template_name = "patient-user.html"

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
            "name": "CT1",
            "location": "综合二层102",
            "order": 189,
            "status": "等待检查",
        }, {
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
            "id":"123",
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
            "name": "B超",
            "price": "199",
        }, {
            "name": "CT",
            "price": "199",
        }, ]

        # 登录人个人信息
        return render(request, PatientWorkMyView.template_name, locals())


class PatientAPI(View):
    def get(self, request):
        # 获取需要查询的信息类型
        query_information = request.GET.get('information')

        # 确诊详情信息查询
        if query_information == "QZXQ":
            quezhen_no = request.GET.get('quezhen_no')
            print("--------------------")
            print(quezhen_no)
            print("--------------------")
            # 给出能给的尽量多的信息就行，以下只是示例
            data = {
                "no": 114514,
                "name": "CCC",
                "gender": "男",
                "age": 18,
                "HZZS": "患者主诉文本",
                "TGJC": "体格检查文本",
                "FBSJ": "发病事件文本",
                "QZ":"确诊文本",
            }

        # 检查详情查询
        elif query_information == "JCXQ":
            pass

        elif query_information == "XXXX":
            pass

        return JsonResponse(data, safe=False) # 这里是要干什么呀
