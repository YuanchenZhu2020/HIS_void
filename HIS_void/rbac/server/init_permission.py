from django.conf import settings


def init_permission(request, user_obj):
    """
    该函数在用户登录后调用，根据用户对象获取：
        1. URL访问权限 <codename>.<url>
        2. 行级资源权限 <app_label>.<model>.<object_id>.<codename>
        3. （菜单对象）
    然后写入 Request.session 中。
    :params: request: Request 请求对象
    :params: user_obj: 用户对象，来自 UserInfo 表
    """
    user_url_permissions = user_obj.get_all_url_permissions()
    user_obj_permissions = user_obj.get_all_obj_permissions()
    # print("URL Perms", user_url_permissions)
    # print("OBJ Perms", user_obj_permissions)

    url_permissions_list = []
    obj_permissions_list = []
    # permission_menu_list = []

    # URL访问权限
    for item in user_url_permissions:
        perm_code, url = item.split('.')
        url_permissions_list.append((perm_code, url))
    # 对象资源权限
    for item in user_obj_permissions:
        app_label, model, object_id, codename = item.split('.')
        obj_permissions_list.append((model, object_id, codename))

    request.session[settings.PERMISSION_URL_KEY] = url_permissions_list
    request.session[settings.PERMISSION_OBJ_KEY] = obj_permissions_list
    # request.session[settings.PERMISSION_MENU_KEY] = menu_permissions_list

