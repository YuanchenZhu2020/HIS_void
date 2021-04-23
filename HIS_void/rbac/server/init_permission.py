from django.conf import settings


def init_permission(request, user_obj):
    """
    该函数在用户登录后调用，根据用户对象获取：
        1. URL访问权限
        2. 行级资源权限
        3. （菜单对象）
    然后写入 Request.session 中。
    :params: request: Request 请求对象
    :params: user_obj: 用户对象，来自 UserInfo 表
    """
    user_url_permissions = user_obj.get_all_url_permissions()

    url_permissions_list = []
    # permission_menu_list = []

    for item in user_url_permissions:
        perm_code, url = item.split('.')
        url_permissions_list.append((perm_code, url))
        # 权限与菜单信息
        # pmd = {
        #     "id": item["permissions__id"],
        #     "title": item["permissions__title"],
        #     "url": url,
        #     "pid_id": item["permissions__pid_id"],
        #     "menu_id": item["permissions__perm_group__menu_id"],
        #     "menu_title": item["permissions__perm_group__menu_title"],
        # }
        # permission_menu_list.append(pmd)

    request.session[settings.PERMISSION_URL_KEY] = url_permissions_list
    # request.session[settings.PERMISSION_MENU_KEY] = permission_menu_list

