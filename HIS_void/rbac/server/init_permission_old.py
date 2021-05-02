from django.conf import settings


def init_permission(request, user_obj):
    """
    该函数在用户登录后调用，根据用户对象获取权限，写入 Request.session 中。
    1. 通过 user_obj 获取角色对象 roles
    2. 根据与 Role 表的 permissions 获取 Permission 表中数据
    :params: request: Request 请求对象
    :params: user_obj: 用户对象，来自 UserInfo 表
    """
    user_permissions = user_obj.roles.values(
        "permissions__id",
        "permissions__title",
        "permissions__url",
        "permissions__create_time",
        "permissions__perm_code",
        "permissions__perm_group_id",
        "permissions__pid_id",
        # "permissions__perm_group__menu_id",
        # "permissions__perm_group__menu_title",
    ).distinct()

    permission_url_list = {}
    # permission_menu_list = []

    for item in user_permissions:
        # 权限绑定的操作和其URL
        perm_group_id = item["permissions__perm_group_id"]
        url           = item["permissions__url"]
        perm_code     = item["permissions__perm_code"]
        if perm_group_id in permission_url_list:
            permission_url_list[perm_group_id]["codes"].append(perm_code)
            permission_url_list[perm_group_id]["urls"].append(url)
        else:
            permission_url_list[perm_group_id] = {
                "codes": [perm_code,],
                "urls": [url,]
            }
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

    request.session[settings.PERMISSION_URL_KEY] = permission_url_list
    # request.session[settings.PERMISSION_MENU_KEY] = permission_menu_list

