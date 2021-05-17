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
    HospitalDoctorView, InhospitalAPI, IndexView, StaffLoginView, StaffLogoutView, ProfileView,
    IndexView, StaffLoginView, StaffLogoutView, ProfileView,
    IndexView, StaffLoginView, StaffLogoutView, NewsView,
    ProfileView,
)
from patient.views import (
    PatientLoginView, PatientRegisterView, ForgotPasswordView,
    PatientView, PatientRegisterSuccessView, PatientDetailsView,
    PatientLoginView, PatientRegisterView, ForgotPasswordView,
    PatientWorkSpaceView, PatientWorkMyView,
)
from outpatient.views import OutpatientView
from inpatient.views import NurseView
from laboratory.views import InspectionView
from internalapi.views import NurseAPI, OutpatientAPI, InspectionAPI, PatientViewAPI, PatientUserAPI

from rbac.management import create_urlpermissions

urlpatterns = [
    path('', IndexView.as_view(), name='index-alias'),
    # 管理员
    path('admin/', admin.site.urls),
    # 主页
    path('index/', IndexView.as_view(), name="index"),
    # 职工登录页面
    path("login-staff/", StaffLoginView.as_view(), name="login-staff"),
    # 患者登录页面
    path("login-patient/", PatientLoginView.as_view(), name="login-patient"),
    # 注册页面
    path('register/', PatientRegisterView.as_view(), name="register"),
    # 注册成功页面
    path('register-success/', PatientRegisterSuccessView.as_view(), name="register-success"),
    # 找回密码页面
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
    # 登出页面
    path('logout/', StaffLogoutView.as_view(), name="logout"),
    # 个人信息页面
    path('profile/', ProfileView.as_view(), name="profile"),
    # 门诊医生工作页面
    path('outpatient-workspace/', OutpatientView.as_view(), name="outpatient-workspace"),
    # 患者未登录首页
    path('patient/', PatientView.as_view(), name="patient"),
    # 患者登录后个人界面
    path('patient-details/', PatientDetailsView.as_view(), name="patient-details"),
    # 护士门诊
    path('nurse-workspace/', NurseView.as_view(), name="nurse-workspace"),
    # 检查检验
    path('inspection-workspace/', InspectionView.as_view(), name="inspection-workspace"),
    # 住院医生
    path('inhospital-doctor/', HospitalDoctorView.as_view(), name="inhospital-doctor"),
    # 查询机器检验的各种信息
    path('InspectionAPI/', InspectionAPI.as_view(), name="InspectionAPI"),
    # 查询门诊医生的各种信息
    path('OutpatientAPI/', OutpatientAPI.as_view(), name="OutpatientAPI"),
    # 保存体征记录的各种信息
    path('NurseAPI/', NurseAPI.as_view(), name="NurseAPI"),
    # 保存个人信息
    path('PatientUserAPI/', PatientUserAPI.as_view(), name="PatientUserAPI"),
    # 挂号API 保存挂号信息
    path('PatientViewAPI/', PatientViewAPI.as_view(), name="PatientViewAPI"),
    # 保存住院医生能查询到的住院人信息
    path('InhospitalAPI/', InhospitalAPI.as_view(), name="InhospitalAPI"),
    # 近期新闻
    path('news/', NewsView.as_view(), name="news"),
]

]

# 每次执行 makemigrations, migrate, runserver 等命令时会执行以下过程，
# 用于及时更新 urlpatterns 的更改，更新 URL 访问权限记录。
from django.apps import apps as global_apps

app_config = global_apps.get_app_config("rbac")
create_urlpermissions(app_config)
