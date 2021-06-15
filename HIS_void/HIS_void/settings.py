"""
Django settings for HIS_void project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rx*$9b3=cd$a=&9p9e1t7k%*r0-sjxanaawmofpg-q-q5pz^k%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "his.formlesslab.top", "82.156.22.48"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Channels App for WebSocket
    'channels',
    # Django Schedule Task
    'django_apscheduler',
    # Role-Based Access Control
    'rbac',
    # 外部接口
    'externalapi',
    # Hospital Iinformation System Gate
    'his',
    # 病人页面
    'patient',
    # 住院
    'inpatient',
    # 门诊
    'outpatient',
    # 药房
    'pharmacy',
    # 检验科
    'laboratory',
    # 内部接口
    'internalapi',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Patient User Middleware
    "patient.middleware.PatientUserMiddleware",
    # RBAC Middleware
    "rbac.middleware.rbac.RBACMiddleware",
]

ROOT_URLCONF = 'HIS_void.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_share'),
    os.path.join(BASE_DIR, "outpatient/static"),
    os.path.join(BASE_DIR, "internalapi/static"),
)

WSGI_APPLICATION = 'HIS_void.wsgi.application'
ASGI_APPLICATION = 'HIS_void.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Auto Field Setting
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth user model
AUTH_USER_MODEL = "rbac.UserInfo"
# Auth backends
AUTHENTICATION_BACKENDS = (
    "rbac.backends.CustomBackends",
)

# Role-Based Access Control
PERMISSION_URL_KEY = "url_key"
PERMISSION_OBJ_KEY = "obj_key"
# PERMISSION_MENU_KEY = "menu_key"

# SAFE_URL = [
#     r"/index/",  # 主页
#     r"/login-staff/",  # 职工登录
#     r"/login-patient/",  # 医生登录
#     r"/logout/",  # 注销
#     r"/register/",  # 注册
#     r"/register-success/",  # 注册成功页面
#     r"/forgot-password/",  # 忘记密码
#     r"/admin/.*",  # 后台管理？
#     r"/workhub/",  # 职工工作中心页面
#     r"/patient/",  # 病人主页
#     r"/patient-details/",  # 病人详细页面
#     r"/nurse-workspace/",  # 护士工作台
#     r"/outpatient-workspace/",  # 门诊医生工作台
#     r"/inpatient-workspace/",  # 住院医生工作台
#     r"/inspection-workspace/",  # 检验医生工作台
#     r"/InspectionAPI/",  # 检验医生数据API
#     r"/OutpatientAPI/",  # 门诊医生数据API
#     r"/NurseAPI/",  # 护士数据API
#     r"/PatientRegisterAPI/",  # 患者挂号查询与提交API
#     r"/InpatientAPI/",  # 住院医生数据API
#     r"/news/",
#     r"/PatientFastRegisterAPI", # 患者快速挂号API
#     r"/PatientTreatmentDetailAPI", # 患者治疗信息查询API
#     r"/PaymentAPI", # 支付接口
#     r"/PaymentNotifyAPI", # 支付成功回调接口
#     r"/payment-check", # 支付验证页面
#     r"/payment-error/", # 支付失败页面
# ]

# RBAC Accessed URLs without Login
SAFE_URL = [
    r"/admin/",  # 后台管理
    r"/admin/login/", # 后台登陆
    r"/", # 主页 alias
    r"/index/",  # 主页
    r"/login-staff/",  # 职工登录
    r"/login-patient/",  # 医生登录
    r"/register/",  # 注册
    r"/register-success/",  # 注册成功页面
    r"/forgot-password/",  # 忘记密码
    r"/patient/",  # 患者挂号页面
    r"/PaymentNotifyAPI/", # 支付成功回调接口
    r"/PatientRegisterAPI/",  # 患者挂号查询与提交API
]

# setup session engine to improve performance
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
# set brawser-length sessions
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# set persistent sessions (1 day = 86400 seconds)
# SESSION_COOKIE_AGE = 86400

# set length of patient id
PATIENT_ID_LEN = 6
# PATIENT_AUTH_USER_MODEL = "patient.PatientUser"


# Django-Scheduler
# Format string for displaying run time timestamps in the Django admin site. The default
# just adds seconds to the standard Django format, which is useful for displaying the timestamps
# for jobs that are scheduled to run on intervals of less than one minute.
# 
# See https://docs.djangoproject.com/en/dev/ref/settings/#datetime-format for format string
# syntax details.
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# Maximum run time allowed for jobs that are triggered manually via the Django admin site, which
# prevents admin site HTTP requests from timing out.
# 
# Longer running jobs should probably be handed over to a background task processing library
# that supports multiple background worker processes instead (e.g. Dramatiq, Celery, Django-RQ,
# etc. See: https://djangopackages.org/grids/g/workers-queues-tasks/ for popular options).
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds


# alipay sandbox
# 支付宝沙箱 APP_ID
ALIPAY_APPID = '2021000117667930'
# 支付宝网站回调 URL 名称
ALIPAY_APP_NOTIFY_URL_NAME = "payment-notify"
# 支付宝同步 return_url 名称
ALIPAY_APP_RETURN_URL_NAME = "payment-check"
# 支付宝订单超时失效时间
ALIPAY_TIMEOUT_MINUTE = 15
# 网站私钥文件路径
APP_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'externalapi/alipay_keys/app_private.key')
# 支付宝公钥文件路径
ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'externalapi/alipay_keys/alipay_public.key')
# 支付宝沙箱的开发模式
ALIPAY_DEBUG = True
# 支付宝沙箱支付网关
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'


# 患者 URL 访问权限
# /logout/
# /patient-details/
# /PatientFastRegisterAPI/
# /PatientTreatmentDetailAPI/

# 角色
#   职工
#       /workhub/
#       /logout/
#   门诊医生
#       /outpatient-workspace/
#       /OutpatientAPI/
#   住院医生
#       /inpatient-workspace/
#       /InpatientAPI/
#   护士
#       /nurse-workspace/
#       /NurseAPI/
# 检验技师
# 财务人员
# 
