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
    ProfileView, OutpatientView, NurseView, InspectionView, InspectionAPI, OutpatientAPI,
    NurseAPI,
)
from patient.views import (
    PatientLoginView, PatientRegisterView, ForgotPasswordView, PatientWorkSpaceView, PatientWorkMyView,
)

urlpatterns = [
    path('', IndexView.as_view(), name=''),
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
    # 找回密码页面
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
    # 登出页面
    path('logout/', StaffLogoutView.as_view(), name="logout"),
    # 个人信息页面
    path('profile/', ProfileView.as_view(), name="profile"),
    # 门诊医生工作页面
    path('outpatient-workspace/', OutpatientView.as_view(), name="outpatient-workspace"),
    # # 患者未登录首页
    # path('patient/', PatientWorkSpaceView.as_view(), name = "patient"),
    # 患者登录后个人界面
    path('patient-user/', PatientWorkSpaceView.as_view(), name="patient-user"),
    # 护士门诊
    path('nurse-workspace/', NurseView.as_view(), name="nurse-workspace"),
    # 检查检验
    path('inspection-workspace/', InspectionView.as_view(), name="inspection-workspace"),
    # 查询机器检验的各种信息
    path('InspectionAPI/', InspectionAPI.as_view(), name="InspectionAPI"),
    # 查询门诊医生的各种信息
    path('OutpatientAPI/', OutpatientAPI.as_view(), name="OutpatientAPI"),
    # 保存体征记录的各种信息
    path('NurseAPI/', NurseAPI.as_view(), name="NurseAPI"),
]
