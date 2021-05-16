from time import sleep

from django.contrib.auth import login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from his.forms import StaffLoginFrom
from patient.models import PatientUser
from rbac.models import UserInfo
from laboratory.models import TestItemType, TestItem
from rbac.server.init_permission import init_permission


class IndexView(View):
    template_name = "index.html"
    staff_next_url_name = "profile"
    patient_next_url_name = "patient-user"

    def get(self, request):
        print("[Index View]", request.user)
        if request.user.is_authenticated:
            # print(type(request.user))
            if isinstance(request.user, UserInfo):
                return redirect(reverse(IndexView.staff_next_url_name))
            elif isinstance(request.user, PatientUser):
                return redirect(reverse(IndexView.patient_next_url_name))
            else:
                return HttpResponse("Fatal Error!")
        else:
            return render(request, IndexView.template_name)


class StaffLoginView(View):
    template_name = "page-login.html"
    staff_next_url_name = "profile"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse(StaffLoginView.staff_next_url_name))
        else:
            loginform = StaffLoginFrom()
            context = {"user_type": "staff", "loginform": loginform}
            return render(request, StaffLoginView.template_name, context)

    def post(self, request):
        # 通过 StaffLoginForm.clean() 方法进行多种验证
        login_info = StaffLoginFrom(data=request.POST)
        # 验证成功
        if login_info.is_valid():
            # 获取用户对象和是否保持登录的标识
            user = login_info.get_user()
            remember_me = login_info.remember_me
            # 登录
            login(request, user)
            # 向 Session 中写入信息
            request.session["username"] = user.get_username()
            request.session["staff_name"] = user.staff.name
            request.session["dept_id"] = user.staff.dept.ug_id
            request.session["title_name"] = user.staff.title.title_name
            request.session["job_name"] = user.staff.job.job_name
            # 获取用户权限，写入 session 中
            init_permission(request, user)
            # print(request.session["url_key"], request.session["obj_key"])
            # 若选择保持登录，则重新设置 session 保存时间为 1 天 (86400 s)
            if remember_me:
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
            return render(request, StaffLoginView.template_name, context)


class StaffLogoutView(View):
    template_name = "index"

    def get(self, request):
        logout(request)
        # request.session.clear()
        return redirect(reverse(StaffLogoutView.template_name))


class ProfileView(View):
    template_name = 'page-profile.html'

    def get(self, request):
        # print("[Session]", request.session)
        if request.user.is_authenticated and isinstance(request.user, UserInfo):
            return render(request, ProfileView.template_name)
        else:
            return redirect(reverse("index"))

    def post(self, request):
        post_dict = dict(request.POST)

        print("````````````````````````````````````````````````")
        print(post_dict)


class OutpatientView(View):
    template_name = 'page-outpatient-workspace.html'

    def get(self, request):
        return render(request, OutpatientView.template_name)


class NurseView(View):
    template_name = 'page-nurse-workspace.html'

    def get(self, request):
        return render(request, NurseView.template_name)


class InspectionView(View):
    template_name = 'page-inspection-workspace.html'

    def get(self, request):
        return render(request, InspectionView.template_name)

class HospitalDoctorView(View):
    template_name = 'page-inhospital-doctor.html'

    def get(self, request):
        return render(request, HospitalDoctorView.template_name)


"""
***************************
        数据查询部分
***************************
"""


# 检中患者数据查询
class InspectionAPI(View):
    def get(self, request):
        query_information = request.GET.get('information')

        # 数据库查询操作
        if query_information == "InspectingInformation":
            p_no = request.GET.get('p_no')
            print(p_no)
            data = {
                "no": 114514,
                "name": "肖云冲",
                "gender": "男",
                "age": 18,
                "JYMC": "血常规",
                "KJSJ": "2021.05.1 20：00",
                "KJYS": "王医生"
            }
        elif query_information == "InspectingPatient":
            data = [
                {
                    "p_no": "183771**",
                    "name": "李国铭",
                    "status": "危机",
                },
                {
                    "p_no": "183771--",
                    "name": "肖云冲",
                    "status": "普通",
                },
                {
                    "p_no": "183771++",
                    "name": "朱元琛",
                    "status": "安全",
                },
            ]
            # 传入医生主键，这样可以有选择的返回病人信息
            d_no = request.GET.get('d_no')
            print(d_no)

        return JsonResponse(data, safe=False)

    def post(self, request):
        print("================================")
        print(request.POST.get('PDXX'))
        print("================================")
        sleep(1)
        return redirect(reverse("inspection-workspace"))


"""
门诊医生工作台数据API
"""


class OutpatientAPI(View):
    def get(self, request):
        # 获取需要查询的信息类型
        query_information = request.GET.get('information')

        # 病历首页信息查询
        if query_information == "BLSY":
            p_no = request.GET.get('p_no')
            print(p_no)
            data = {
                "no": 114514,
                "name": "肖云冲",
                "gender": "男",
                "age": 18,
                "HZZS": "患者主诉文本",
                "ZLQK": "治疗情况文本",
                "JWBS": "既往病史文本",
                "GMBS": "过敏病史文本",
                "TGJC": "体格检查文本",
                "FBSJ": "发病事件文本",
            }

        # 待诊患者信息查询
        elif query_information == "DZHZ":
            data = [
                {
                    "p_no": "183771**",
                    "name": "李国铭",
                    "status": "危机",
                },
                {
                    "p_no": "183771--",
                    "name": "肖云冲",
                    "status": "普通",
                },
                {
                    "p_no": "183771++",
                    "name": "朱元琛",
                    "status": "安全",
                },
            ]
            # 传入医生主键，这样可以有选择的返回病人信息
            d_no = request.GET.get('d_no')
            print(d_no)

        # 诊中患者信息查询
        elif query_information == "ZZHZ":
            data = [
                {
                    "p_no": "183771**",
                    "name": "李国铭",
                    "status": "危机",
                },
                {
                    "p_no": "183771--",
                    "name": "肖云冲",
                    "status": "普通",
                },
                {
                    "p_no": "183771++",
                    "name": "朱元琛",
                    "status": "安全",
                },
            ]
            # 传入医生主键，这样可以有选择的返回病人信息
            d_no = request.GET.get('d_no')
            print(d_no)

        # 检查结果信息查询
        elif query_information == "JCJG":
            data = [

            ]

        # 药品检索
        elif query_information == "CFKJ":
            data = [
                {'name': "多塞平", 'price': 41, 'number': 100, },
                {'name': "艾司西酞普兰", 'price': 42, 'number': 100, },
                {'name': "帕罗西汀", 'price': 43, 'number': 100, },
                {'name': "氟西汀", 'price': 44, 'number': 100, },
                {'name': "度洛西汀", 'price': 45, 'number': 100, },
                {'name': "氟伏沙明", 'price': 46, 'number': 100, },
            ]

        return JsonResponse(data, safe=False)

    def post(self, request):
        print("================================")
        print(request.POST.get('CGJY'))
        print("================================")
        sleep(1)
        return redirect(reverse("outpatient-workspace"))


"""
护士工作台数据API
"""

class NurseAPI(View):
    def get(self, request):
        # 获取需要查询的信息类型
        query_information = request.GET.get('information')

        # 医嘱处理信息查询
        if query_information == "QZXQ":
            p_no = request.GET.get('p_no')
            print(p_no)
            # 数据库查询语句
            data = {
                "no": 114514,
                "name": "肖云冲",
                "gender": "男",
                "age": 18,
                "HZZS": "患者主诉文本",
                "ZLQK": "治疗情况文本",
                "JWBS": "既往病史文本",
                "GMBS": "过敏病史文本",
                "TGJC": "体格检查文本",
                "FBSJ": "发病事件文本",
            }
        return JsonResponse(data, safe=False)


# 住院医生工作台数据
class InhospitalAPI(View):
    def get(self, request):
        # 获取需要查询的信息类型
        query_information = request.GET.get('information')

        #
        if query_information == "ZZHZ":
            p_no = request.GET.get('p_no')
            print(p_no)
            # 数据库查询语句
            data = [{
                "p_no": 114514,
                "name": "发多冲",
                "bed":123,
            },{
                "p_no": 11343,
                "name": "肖大赛",
                "bed":543,
            },{
                "p_no": 114424,
                "name": "阿凡达",
                "bed":64,
            }]
        return JsonResponse(data, safe=False)
