# Generated by Django 3.1.7 on 2021-06-05 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import rbac.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='对象权限名称')),
                ('object_id', models.CharField(max_length=255, verbose_name='对象ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_perm_set', related_query_name='object_prems', to='auth.permission', verbose_name='权限')),
            ],
            options={
                'verbose_name': '对象权限',
                'verbose_name_plural': '对象权限',
                'ordering': ['permission__content_type__app_label', 'permission__content_type__model', 'object_id'],
                'unique_together': {('permission', 'object_id')},
            },
        ),
        migrations.CreateModel(
            name='PermissionsMixin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='超级用户具有全部权限。', verbose_name='超级用户')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='角色名')),
                ('description', models.TextField(default='', max_length=300, verbose_name='角色描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('obj_permissions', models.ManyToManyField(blank=True, help_text='该角色拥有的对象资源权限', related_name='role_set', related_query_name='roles', to='rbac.ObjectPermission', verbose_name='对象资源权限')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
            },
        ),
        migrations.CreateModel(
            name='URLPermission',
            fields=[
                ('codename', models.CharField(help_text='简要概括URL访问权限作用的对象，建议使用英文单词和下划线。', max_length=64, primary_key=True, serialize=False, verbose_name='权限代码')),
                ('url_regex', models.CharField(help_text='用于匹配指定URL的正则表达式。', max_length=128, unique=True, verbose_name='URL')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'URL访问权限',
                'verbose_name_plural': 'URL访问权限',
                'ordering': ['codename', 'url_regex'],
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('permissionsmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='rbac.permissionsmixin')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(help_text='以 6 位数字的工号作为登录账户名。', max_length=6, primary_key=True, serialize=False, verbose_name='登录账号')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('is_active', models.BooleanField(default=True, help_text='决定该用户是否为活动账户。', verbose_name='活动账户')),
                ('is_admin', models.BooleanField(default=False, help_text='决定该用户是否能够访问 /admin 页面。', verbose_name='管理员')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
            bases=('rbac.permissionsmixin', models.Model),
            managers=[
                ('objects', rbac.models.UserInfoManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('ug_id', models.BigAutoField(help_text='用户组编号，取值范围为 1 ~ Inf。', primary_key=True, serialize=False, verbose_name='用户组编号')),
                ('name', models.CharField(help_text='科室、部门或项目组名称。', max_length=32, unique=True, verbose_name='用户组名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('obj_permissions', models.ManyToManyField(blank=True, help_text='该用户组拥有的对象资源权限', related_name='usergroup_set', related_query_name='usergroups', to='rbac.ObjectPermission', verbose_name='对象资源权限')),
                ('roles', models.ManyToManyField(blank=True, help_text='用户组所拥有的角色，用户组能够获取所拥有角色的全部权限。', related_name='usergroup_set', related_query_name='usergroups', to='rbac.Role', verbose_name='角色')),
                ('url_permissions', models.ManyToManyField(blank=True, help_text='用户组具有的全部URL访问权限。', related_name='usergroup_set', related_query_name='usergroups', to='rbac.URLPermission', verbose_name='URL访问权限')),
            ],
            options={
                'verbose_name': '用户组',
                'verbose_name_plural': '用户组',
            },
            managers=[
                ('objects', rbac.models.GroupManager()),
            ],
        ),
        migrations.AddField(
            model_name='role',
            name='url_permissions',
            field=models.ManyToManyField(blank=True, help_text='该角色拥有的URL访问权限', related_name='role_set', related_query_name='roles', to='rbac.URLPermission', verbose_name='URL访问权限'),
        ),
        migrations.AddField(
            model_name='permissionsmixin',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='用户所属的用户组，用户能够获取所属用户组的全部权限。', related_name='user_set', related_query_name='users', to='rbac.UserGroup', verbose_name='用户组'),
        ),
        migrations.AddField(
            model_name='permissionsmixin',
            name='obj_permissions',
            field=models.ManyToManyField(blank=True, help_text='该用户拥有的对象资源权限', related_name='user_set', related_query_name='users', to='rbac.ObjectPermission', verbose_name='对象资源权限'),
        ),
        migrations.AddField(
            model_name='permissionsmixin',
            name='roles',
            field=models.ManyToManyField(blank=True, help_text='用户所拥有的角色，用户能够获取所拥有角色的全部权限。', related_name='user_set', related_query_name='users', to='rbac.Role', verbose_name='角色'),
        ),
        migrations.AddField(
            model_name='permissionsmixin',
            name='url_permissions',
            field=models.ManyToManyField(blank=True, help_text='该用户具有的所有URL访问权限。', related_name='user_set', related_query_name='users', to='rbac.URLPermission', verbose_name='URL访问权限'),
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateTimeField(auto_now_add=True, verbose_name='登录时间')),
                ('ip_address', models.GenericIPAddressField(verbose_name='登录IP')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户账户')),
            ],
            options={
                'verbose_name': '登录日志',
                'verbose_name_plural': '登录日志',
                'unique_together': {('user', 'login_time')},
            },
        ),
    ]
