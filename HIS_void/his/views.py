import math

from django.contrib.auth import login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from his.forms import StaffLoginFrom
from his.models import Department, Notice
from patient.models import PatientUser
from rbac.models import UserInfo
from laboratory.models import TestItemType, TestItem
from rbac.decorators import staff_login_required
from rbac.server.init_permission import init_permission


class IndexView(View):
    """
    HIS登录主页视图函数
    """
    template_name = "index.html"
    staff_next_url_name = "workhub"
    patient_next_url_name = "patient-details"
    error_412_template = "page-error-412.html"

    def get(self, request):
        # print("[Index View]", request.user)
        if request.user.is_authenticated:
            if isinstance(request.user, UserInfo):
                return redirect(reverse(IndexView.staff_next_url_name))
            elif isinstance(request.user, PatientUser):
                return redirect(reverse(IndexView.patient_next_url_name))
            else:
                return render(request, IndexView.error_412_template)
        else:
            return render(request, IndexView.template_name)


class StaffLoginView(View):
    """
    职工登录页面视图
    """
    template_name = "page-login.html"
    staff_next_url_name = "workhub"
    error_wrong_user_login_template = "wrong-user-login-error.html"
    error_412_template = "page-error-412.html"

    def get(self, request):
        if request.user.is_authenticated:
            if isinstance(request.user, UserInfo):
                return redirect(reverse(StaffLoginView.staff_next_url_name))
            elif isinstance(request.user, PatientUser):
                return render(request, StaffLoginView.error_wrong_user_login_template)
            else:
                return render(request, StaffLoginView.error_412_template)
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
            request.session["dept_id"] = user.staff.dept.usergroup.ug_id
            request.session["title_name"] = user.staff.title.title_name
            request.session["job_name"] = user.staff.job.job_name
            # print(dict(request.session))
            # 获取用户权限，写入 session 中
            init_permission(request, user)
            # print(request.session["url_key"], request.session["obj_key"])
            # 若选择保持登录，则重新设置 session 保存时间为 1 天 (86400 s)
            if remember_me:
                request.session.set_expiry(86400)
            # 浏览器关闭则删除 session
            else:
                request.session.set_expiry(0)
            return redirect(reverse(StaffLoginView.staff_next_url_name))
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
    """
    职工登出视图函数
    """
    template_name = "index"

    def get(self, request):
        logout(request)
        # request.session.clear()
        return redirect(reverse(StaffLogoutView.template_name))


@method_decorator(staff_login_required(login_url = "/login-staff"), name = "get")
@method_decorator(staff_login_required(login_url = "/login-staff"), name = "post")
class WorkHubView(View):
    """
    职工工作中心
    """
    template_name = 'workhub.html'

    def get(self, request):
        # print("[Session]", request.session)
        dept_id = request.session.get('dept_id')
        staff_dept = Department.objects.get_by_dept_id(dept_id)
        news = []
        notices = staff_dept.notice_set_recv.all().order_by("-send_time")[0:4]
        for note in notices:
            news.append({
                "send_time": note.send_time, 
                "content": note.content
            })
        return render(request, WorkHubView.template_name, context = {'news': news})

    def post(self, request):
        post_dict = dict(request.POST)

        print("````````````````````````````````````````````````")
        print(post_dict)


class NewsView(View):
    template_name = "news.html"

    HISTORY_NEWS_CACHE = None
    CACHE_DATE = None

    # 每页新闻数
    PAGE_NONTICES = 10

    def get(self, request):
        """
        通知页面视图函数
        """
        news = []
        dept_id = request.session.get("dept_id")
        # 查询并合并当天通知
        news += self.query_today_notices(dept_id)
        # 查询并合并历史通知
        news += self.query_history_notices(dept_id)
        # 构造 context
        context = {"news": news, "page_num": math.ceil(len(news) / NewsView.PAGE_NONTICES)}
        return render(request, NewsView.template_name, context = context)
    
    def query_history_notices(self, dept_id):
        """
        查询历史通知消息，按时间降序排序。
        """
        history_news = []
        today = timezone.localdate()
        staff_dept = Department.objects.get_by_dept_id(dept_id)
        # 更新历史通知缓存
        if NewsView.CACHE_DATE is None or NewsView.CACHE_DATE < today:
            history_notices = staff_dept.notice_set_recv.all().filter(
                send_time__date__lt = today
            ).order_by("-send_time")
            for note in history_notices:
                history_news.append({
                    "send_time": note.send_time, 
                    "content": note.content
                })
            NewsView.HISTORY_NEWS_CACHE = history_news
            NewsView.CACHE_DATE = today
        return NewsView.HISTORY_NEWS_CACHE

    def query_today_notices(self, dept_id):
        """
        查询当天通知，按时间降序排序。

        :param dept_id: Department id.
        :returns: list of dict {'send_time':***, 'content':***}
        """
        news = []
        today = timezone.localdate()
        staff_dept = Department.objects.get_by_dept_id(dept_id)
        # 查询当天通知
        notices = staff_dept.notice_set_recv.all().filter(
            send_time__date = today
        ).order_by("-send_time")
        for note in notices:
            news.append({
                "send_time": note.send_time, 
                "content": note.content
            })
        return news

    def post(self, request):
        """
        通知分页查询API
        """
        page_num = request.POST.get("page")

        dept_id = request.session.get("dept_id")
        notices = self.query_today_notices(dept_id)
        notices += self.query_today_notices(dept_id)
        news_num = len(notices)
        st = NewsView.PAGE_NONTICES * (page_num - 1)
        ed = min(NewsView.PAGE_NEWS * page_num, news_num)

        # 分页起始位置超过通知数量，返回空字符串
        if st >= news_num:
            return JsonResponse("", safe = False)
        return JsonResponse(notices[st:ed], safe = False)
