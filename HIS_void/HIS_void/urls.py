"""HIS_void URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from his.views import (
    IndexView, StaffLoginView, StaffLogoutView, 
    ProfileView, OutpatientView
)
from patient.views import (
    PatientLoginView, PatientRegisterView, ForgotPasswordView, 
    PatientWorkSpaceView, PatientWorkMyView, PatientRegisterSuccessView
)


urlpatterns = [
    path('', IndexView.as_view(), name = 'index-alias'),
    # 管理员
    path('admin/', admin.site.urls),
    # 主页
    path('index/', IndexView.as_view(), name = "index"),
    # 职工登录页面
    path("login-staff/", StaffLoginView.as_view(), name = "login-staff"),
    # 患者登录页面
    path("login-patient/", PatientLoginView.as_view(), name = "login-patient"),
    # 注册页面
    path('register/', PatientRegisterView.as_view(), name = "register"),
    path('register-success/', PatientRegisterSuccessView.as_view(), name = "register-success"),
    # 找回密码页面
    path('forgot-password/', ForgotPasswordView.as_view(), name = "forgot-password"),
    # 登出页面
    path('logout/', StaffLogoutView.as_view(), name = "logout"),
    # 个人信息页面
    path('profile/', ProfileView.as_view(), name = "profile"),
    # 门诊医生工作页面
    path('outpatient-workspace/', OutpatientView.as_view(), name = "outpatient-workspace"),
    # # 患者未登录首页
    # path('patient/', PatientWorkSpaceView.as_view(), name = "patient"),
    # 患者登录后个人界面
    path('patient-user/', PatientWorkSpaceView.as_view(), name = "patient-user"),
]

# 通过 HIS_void.url 自动添加 URL Permissions
def create_urlpermissions():
    from rbac.models import URLPermission
    from django.utils import timezone

    create_time = timezone.now()
    old_urlps = set(URLPermission.objects.all().values_list("name", "url"))
    new_urlps = set((urlp.pattern.name, urlp.pattern._route) for urlp in urlpatterns)
    # 删除被删除的URL对应的URL访问权限
    delete_urlperms = old_urlps - new_urlps
    delete_urls = [nu[1] for nu in delete_urlperms]
    URLPermission.objects.filter(url__in = delete_urls).delete()
    # 添加新增的URL对应的URL访问权限
    add_urlps = new_urlps - old_urlps
    if len(add_urlps) > 0:
        add_url_objs = [
            URLPermission(
                name = urlp[0],
                url = '/' + urlp[1],
                codename = "access-" + urlp[0],
                create_time = create_time
            )
            for urlp in add_urlps 
                if urlp[0] is not None
        ]
        URLPermission.objects.bulk_create(add_url_objs)

create_urlpermissions()
