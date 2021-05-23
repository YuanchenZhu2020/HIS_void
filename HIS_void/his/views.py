from time import sleep

from django.contrib.auth import login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from his.forms import StaffLoginFrom
from his.models import Notice
from patient.models import PatientUser
from rbac.models import UserInfo
from laboratory.models import TestItemType, TestItem
from rbac.server.init_permission import init_permission


class IndexView(View):
    template_name = "index.html"
    staff_next_url_name = "profile"
    patient_next_url_name = "patient"

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
            request.session["name"] = user.staff.name
            request.session["dept_id"] = user.staff.dept.dept.ug_id
            request.session["title_name"] = user.staff.title.title_name
            request.session["job_name"] = user.staff.job.job_name
            print(dict(request.session))
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
    template_name = 'profile.html'

    def get(self, request):
        # print("[Session]", request.session)
        for item in dict(request.session):
            print(item, ': ', request.session[item])
        news = []
        if request.user.is_authenticated and isinstance(request.user, UserInfo):
            notices = Notice.objects.filter(dept_id__exact=request.session.get('dept_id')).order_by('send_time')[0:4]
            for note in notices:
                note_info = {'send_time': note.send_time.strftime('%m/%d'), 'content': note.content}
                news.append(note_info)

            return render(request, ProfileView.template_name, context={'news': news})
        else:
            return redirect(reverse("index"))

    def post(self, request):
        post_dict = dict(request.POST)

        print("````````````````````````````````````````````````")
        print(post_dict)


class NewsView(View):
    template_name = 'news.html'

    def get(self, request):
        news = []
        notices = Notice.objects.filter(dept_id__exact=request.session.get('dept_id')).order_by('send_time')
        for note in notices:
            note_info = {'send_time': note.send_time.strftime('%m/%d'), 'content': note.content}
            news.append(note_info)
        return render(request, NewsView.template_name, context={'news': news})
