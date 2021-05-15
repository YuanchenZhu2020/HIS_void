import re

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.middleware.csrf import rotate_token
from django.utils.crypto import constant_time_compare

from .signals import patient_logged_in, patient_logged_out, patient_login_failed

SESSION_KEY = '_patient_auth_user_id'
HASH_SESSION_KEY = '_auth_user_hash'
REDIRECT_FIELD_NAME = 'next'

USER_MODEL = "patient.PatientUser"
PERM_MODEL = "patient.PatientURLPermission"


def get_user_model():
    """
    返回对应路径的用户模型。
    """
    try:
        return django_apps.get_model(USER_MODEL, require_ready = False)
    except ValueError:
        raise ImproperlyConfigured("用户模型必须以 'app_label.model_name' 的格式给出")
    except LookupError:
        raise ImproperlyConfigured(
            "用户验证模型 '{}' 还没有安装".format(USER_MODEL)
        )

def _clean_credentials(credentials):
    """
    Clean a dictionary of credentials of potentially sensitive info before
    sending to less secure functions.

    Not comprehensive - intended for user_login_failed signal
    """
    SENSITIVE_CREDENTIALS = re.compile('api|token|key|secret|password|signature', re.I)
    CLEANSED_SUBSTITUTE = '********************'
    for key in credentials:
        if SENSITIVE_CREDENTIALS.search(key):
            credentials[key] = CLEANSED_SUBSTITUTE
    return credentials

def _get_user_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    return get_user_model()._meta.pk.to_python(request.session[SESSION_KEY])

def _authenticate(request, username = None, password = None, **kwargs):
    print("[]", username, password)
    if username is None:
        username = kwargs.get(get_user_model().USERNAME_FIELD)
    if username is None or password is None:
        return
    try:
        user = get_user_model()._default_manager.get_by_natural_key(username)
    except get_user_model().DoesNotExist:
        # Run the default password hasher once to reduce the timing
        # difference between an existing and a nonexistent user (#20760).
        get_user_model()().set_password(password)
    else:
        if user.check_password(password):
            return user

def authenticate(request = None, **credentials):
    """
    If the given credentials are valid, return a User object.
    """
    try:
        user = _authenticate(request, **credentials)
    except PermissionDenied:
        patient_login_failed.send(
            sender = __name__, 
            credentials = _clean_credentials(credentials), 
            request = request
        )
    if user is None:
        patient_login_failed.send(
            sender = __name__, 
            credentials = _clean_credentials(credentials), 
            request = request
        )
    # print("[authenticate]", user)
    return user

def init_patient_url_permission(request, user):
    """
    使用与 RBAC.UserInfo 相同的权限格式进行患者登录的初始化。其中：
        1. URL 访问权限为患者URL权限数据库中的全部权限
        2. 对象资源权限留空
        3. 从代码层面“写死”患者查询数据的条件，即只能查询本账号 patient_id 的数据
    """
    all_urlperms = user.get_all_url_permissions()
    
    url_permissions_list = []
    obj_permissions_list = []

    # URL访问权限
    for item in all_urlperms:
        perm_code, url = item.split('.')
        url_permissions_list.append((perm_code, url))
    
    request.session[settings.PERMISSION_URL_KEY] = url_permissions_list
    request.session[settings.PERMISSION_OBJ_KEY] = obj_permissions_list

def login(request, user):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    """
    session_auth_hash = ''
    if user is None:
        user = request.user
    if hasattr(user, 'get_session_auth_hash'):
        session_auth_hash = user.get_session_auth_hash()

    if SESSION_KEY in request.session:
        if _get_user_session_key(request) != user.pk or (
                session_auth_hash and
                not constant_time_compare(request.session.get(HASH_SESSION_KEY, ''), session_auth_hash)):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            print("[FLUSH]")
            request.session.flush()
    else:
        request.session.cycle_key()

    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[HASH_SESSION_KEY] = session_auth_hash
    # print("[login]", request.session[SESSION_KEY], request.session[HASH_SESSION_KEY])
    if hasattr(request, 'user'):
        request.user = user
    rotate_token(request)
    print("[login]", request.user)
    patient_logged_in.send(sender = user.__class__, request = request, user = user)

# 未测试
def logout(request):
    """
    Remove the authenticated user's ID from the request and flush their session
    data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if not getattr(user, 'is_authenticated', True):
        user = None
    patient_logged_out.send(sender = user.__class__, request = request, user = user)
    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

def _get_user(user_id):
    """
    通过用户模型主键值获取用户对象，
    如果用户对象能够验证，则返回，否则返回None
    """
    try:
        user = get_user_model()._default_manager.get(pk = user_id)
    except get_user_model().DoesNotExist:
        return None
    return user

def get_user(request):
    """
    获取与 request.session 中对应的 PatientUser 实例。
    如果没有找到对应的实例，则返回 AnonymousUser
    """
    from django.contrib.auth.models import AnonymousUser
    user = None
    try:
        user_id = _get_user_session_key(request)
    except KeyError:
        pass
    else:
        user = _get_user(user_id)
        # Verify the session
        if hasattr(user, 'get_session_auth_hash'):
            session_hash = request.session.get(HASH_SESSION_KEY)
            session_hash_verified = session_hash and constant_time_compare(
                session_hash,
                user.get_session_auth_hash()
            )
            if not session_hash_verified:
                if not (
                    session_hash and
                    hasattr(user, '_legacy_get_session_auth_hash') and
                    constant_time_compare(session_hash, user._legacy_get_session_auth_hash())
                ):
                    request.session.flush()
                    user = None

    return user or AnonymousUser()

# 未测试
def update_session_auth_hash(request, user):
    """
    Updating a user's password logs out all sessions for the user.

    Take the current request and the updated user object from which the new
    session hash will be derived and update the session hash appropriately to
    prevent a password change from logging out the session from which the
    password was changed.
    """
    request.session.cycle_key()
    if hasattr(user, 'get_session_auth_hash') and request.user == user:
        request.session[HASH_SESSION_KEY] = user.get_session_auth_hash()


default_app_config = "patient.apps.PatientConfig"
