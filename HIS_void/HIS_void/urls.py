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

from his.views import IndexView, LoginView, RegisterView
from patient.views import PatientLoginView

urlpatterns = [
    # 管理员
    path('admin/', admin.site.urls),
    # 主页
    path('index/', IndexView.as_view(), name="index"),
    # 职工登录页面
    path("login-staff/", LoginView.as_view(), name="login-staff"),
    # 患者登录页面
    path("login-patient/", PatientLoginView.as_view(), name="login-patient"),
    # 注册页面
    path("register/", RegisterView.as_view(), name="register"),
]
